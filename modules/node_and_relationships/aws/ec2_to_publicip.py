from modules.node_and_relationships.aws.nodes import BaseEC2Node, BasePublicIP
from modules.node_and_relationships.node_and_relationships_runner import NodesAndRelationshipsBase, JoinTopics


class EC2ToPublicIP(NodesAndRelationshipsBase):
    def get_relation_name(self):
        return "EC2ToPublicIP"

    @staticmethod
    def should_cache():
        return False

    def init(self):
        streams = ['ec2_gather']

        def get_join_key(item):
            if 'PublicIpAddress' in item:
                return item['PublicIpAddress']
            else:
                return -1

        def get_nodes(items):
            return [BaseEC2Node(items[0]['InstanceId']), BasePublicIP(items[0]['PublicIpAddress'])]

        jp = JoinTopics(self.storage, streams, [get_join_key], 'Ec2PublicIP', get_nodes)
        jp.run()


