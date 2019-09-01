from modules import simple_storage
from modules.api_runner.aws import run_single_region
from modules.info_gather.aws.aws_base import AWSBaseRunner
from modules.info_gather.base_runner import BaseInfoGather


class IamGather(AWSBaseRunner):
    def init(self):
        self.list_roles()
        self.list_users()

    def get_topic_name(self):
        return 'iam_gather'

    def list_users(self):
        all_users = run_single_region('iam', 'list_users', {})
        for user in all_users['Users']:
            self.save_data(user, simple_storage.where('UserName') == user['UserName'], 'users')
            username = user['UserName']
            self.list_access_keys(username)

    def list_roles(self):
        all_roles = run_single_region('iam', 'list_roles', {})
        for role in all_roles['Roles']:
            self.save_data(role, simple_storage.where('RoleName') == role['RoleName'], 'roles')

    def list_access_keys(self, user_name):
        all_keys = run_single_region('iam', 'list_access_keys', {'UserName': user_name})
        for key in all_keys["AccessKeyMetadata"]:
            self.save_data(key, simple_storage.where('AccessKeyId') == key['AccessKeyId'], 'access_keys')




