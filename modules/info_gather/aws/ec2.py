from modules import simple_storage
from modules.api_runner.aws import run_api_cross_region
from modules.info_gather.aws.aws_base import AWSBaseRunner


class Ec2Gather(AWSBaseRunner):
    def get_topic_name(self):
        return 'ec2_gather'

    def init(self):
        self.get_all_instances()

    def get_all_instances(self, filter={}):
        all_instances = run_api_cross_region('ec2', 'describe_instances', filter)
        all_instance_ids = set([])
        for region in all_instances:
            for resevation in all_instances[region]['Reservations']:
                for instance in resevation['Instances']:
                    instance['region'] = region
                    all_instance_ids.add(instance['InstanceId'])
                    self.save_data(instance, simple_storage.where('InstanceId') == instance['InstanceId'])

