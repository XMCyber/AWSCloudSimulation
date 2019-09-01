import time
from datetime import datetime
from datetime import timedelta
import gzip
import json
import boto3
from tinydb import where
import asyncio
from modules import simple_storage
from modules.info_gather.aws.aws_base import AWSBaseRunner
from modules.info_gather.base_runner import BaseInfoGather
from modules import config

'''
class CloudtrailGather(BaseInfoGather):
    def get_topic_name(self):
        return 'cloudtrail'

    def init(self):
        CloudtrailGather.get_all_logs()

    @staticmethod
    def get_all_logs():
        #{'LookupAttributes': [{'AttributeKey': 'Username', 'AttributeValue': 'yaron@xmcyber.com'}]}
        all_logs = modules.api_runner.run_api_paginated_cross_region('cloudtrail', 'lookup_events', {})
        user_to_ip = {}
        events_count = 0
        for region in all_logs:
            for events in all_logs[region]:
                print("Process Events", events_count)
                print("Last Date", events['Events'][0]['EventTime'])
                for event in events['Events']:
                    events_count = events_count + 1
                    #simple_storage.insert("cloudtrail", event)
                    if 'Username' not in event:
                        continue
                    if event['Username'] not in user_to_ip:
                        user_to_ip[event['Username']] = set([])
                    json_event = json.loads(event['CloudTrailEvent'])
                    user_to_ip[event['Username']].add(json_event['sourceIPAddress'])
        j = 0
'''


class CloudtrailGather(AWSBaseRunner):
    def handle_event(self, event):
        return False

    def get_topic_name(self):
        return 'cloudtrail'

    async def init(self):
        await self.get_all_logs()

    async def get_all_logs(self):
        if config.config['AWS']['CLOUDTRAIL']['DISABLE']:
            return

        my_stream_name = config.config['AWS']['CLOUDTRAIL']['STREAM_NAME']

        kinesis_client = boto3.client('kinesis', region_name=config.config['AWS']['CLOUDTRAIL']['KINESIS_REGION'])

        response = kinesis_client.describe_stream(StreamName=my_stream_name)

        my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']

        shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name,
                                                           ShardId=my_shard_id,
                                                           ShardIteratorType='AT_TIMESTAMP',
                                                           Timestamp=datetime.now() - timedelta(hours=3))

        record_response = {}
        record_response['NextShardIterator'] = shard_iterator['ShardIterator']
        count = 0
        events = set()
        user_to_ip = {}
        while 'NextShardIterator' in record_response:
            await asyncio.sleep(1)
            CloudtrailGather.update_db(user_to_ip)
            record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'])
            if len(record_response['Records']) == 0:
                print("zero")
                #print(list(events))
                break

            for record in record_response['Records']:
                record_json = json.loads(gzip.decompress(record['Data']))
                for log in record_json['logEvents']:
                    try:
                        count = count + 1
                        log = json.loads(log['message'])
                        #self.send_event(log)
                        if 'eventName' in log:
                            events.add(log['eventName'])
                        if 'sourceIPAddress' in log:
                            if 'userName' in log['userIdentity']:
                                username = log['userIdentity']['userName']
                            elif 'userName' in log['userIdentity']['sessionContext']:
                                username = log['userIdentity']['sessionContext']['userName']
                            elif 'sessionIssuer' in log['userIdentity']['sessionContext']:
                                username = log['userIdentity']['sessionContext']['sessionIssuer']['userName']
                            else:
                                continue
                            if username not in user_to_ip:
                                user_to_ip[username] = set([])
                            user_to_ip[username].add(log['sourceIPAddress'])
                    except Exception as e:
                        print("Err", e)

            # wait for 5 seconds
            print("count", count)

    @staticmethod
    def update_db(state):
        for key in state:
            simple_storage.upsert('user_to_ip', {'username': key, 'ips': list(state[key])}, where('username') == key)


    #ec = EchoConsumer('cloudtrail-logs', 'shardId-000000000000', 'LATEST')
        #ec.run()
