from modules import simple_storage
from modules.api_runner.aws import run_api_cross_region
from modules.info_gather.aws.aws_base import AWSBaseRunner
from modules.info_gather.base_runner import BaseInfoGather


class LambdaGather(AWSBaseRunner):
    def get_topic_name(self):
        return 'lambda_function'

    def init(self):
        self.get_all_lambda()

    def get_all_lambda(self):
        lambdas_per_region = run_api_cross_region('lambda', 'list_functions', {})
        for region in lambdas_per_region:
            for function in lambdas_per_region[region]['Functions']:
                self.save_data(function, simple_storage.where('FunctionArn') == function['FunctionArn'])
