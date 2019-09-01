from modules.node_and_relationships.aws.nodes import BaseRoleNode, BaseLambdaNode
from modules.node_and_relationships.node_and_relationships_runner import NodesAndRelationshipsBase, JoinTopics


class LambdaToRole(NodesAndRelationshipsBase):
    def get_relation_name(self):
        return "LambdaToRole"

    @staticmethod
    def should_cache():
        return False

    def init(self):

        streams = ['lambda_function']

        def get_join_key(item):
            if 'Role' in item:
                return item['Role']
            else:
                return -1

        def get_nodes(items):
            return [BaseLambdaNode(items[0]['FunctionArn']), BaseRoleNode(items[0]['Role'])]

        jp = JoinTopics(self.storage, streams, [get_join_key], 'LambdaFunctionRole', get_nodes)
        jp.run()
