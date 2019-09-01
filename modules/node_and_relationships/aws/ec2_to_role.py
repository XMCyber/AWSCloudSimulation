from modules import simple_storage
from modules.node_and_relationships.aws.nodes import BaseEC2Node, BaseRoleNode
from modules.node_and_relationships.node_and_relationships_runner import NodesAndRelationshipsBase, JoinTopics


class EC2ToRole(NodesAndRelationshipsBase):
    def get_relation_name(self):
        return "Ec2MachineRole"

    @staticmethod
    def should_cache():
        return False

    def init(self):

        streams = ['ec2_gather']

        def get_join_key(item):
            if 'IamInstanceProfile' in item and 'Arn' in item['IamInstanceProfile']:
                return item['IamInstanceProfile']['Arn']
            else:
                return -1

        def get_nodes(items):
            return [BaseEC2Node(items[0]['InstanceId']), BaseRoleNode(items[0]['IamInstanceProfile']['Arn'])]

        jp = JoinTopics(self.storage, streams, [get_join_key], 'Ec2MachineRole', get_nodes)
        jp.run()

