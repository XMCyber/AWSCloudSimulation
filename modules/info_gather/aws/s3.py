from modules import simple_storage
from modules.api_runner.aws import run_single_region
from modules.info_gather.aws.aws_base import AWSBaseRunner
from modules.info_gather.base_runner import BaseInfoGather


class S3Gather(AWSBaseRunner):
    def handle_event(self, event):
        return False

    def get_topic_name(self):
        return 's3'

    def init(self):
        self.get_all_buckets()

    def get_all_buckets(self):
        all_buckets = run_single_region('s3', 'list_buckets', {})
        for bucket in all_buckets['Buckets']:
            self.save_data(bucket, simple_storage.where('Name') == bucket['Name'])