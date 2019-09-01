from modules import simple_storage
from modules.info_gather.base_runner import DATA_CLASS_MAPPING
from modules.node_and_relationships.aws.nodes import BaseRoleNode, BaseIamAccessKey
from modules.node_and_relationships.node_and_relationships_runner import NodesAndRelationshipsBase, JoinTopics


class AccessKeyToUser(NodesAndRelationshipsBase):
    def get_relation_name(self):
        return "AccessKeyToUser"

    @staticmethod
    def should_cache():
        return False

    def init(self):

        streams = ['iam_gatheraccess_keys', 'iam_gatherusers']

        def get_join_access_key(item):
            if 'UserName' in item:
                return item['UserName']
            else:
                return -1

        def get_join_user_key(item):
            if 'UserName' in item:
                return item['UserName']
            else:
                return -1

        def get_nodes(items):
            return [BaseIamAccessKey(items[0]['AccessKeyId']), BaseRoleNode(items[1]['Arn'])]

        jp = JoinTopics(self.storage, streams, [get_join_access_key, get_join_user_key], 'UserAccessKey', get_nodes)
        jp.run()


