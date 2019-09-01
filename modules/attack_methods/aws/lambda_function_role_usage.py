from modules.attack_methods.base_neo4j import BaseAttackMethod


class LambdaRoleUsage(BaseAttackMethod):
    def get_edge_types(self):
        return ['LambdaFunctionRole']

    def get_attack_difficult(self):
        return 10

    def get_attack_name(self):
        return "LambdaApipaSteal"

    def get_target_node(self):
        return 'AWSLambda'

    def get_source_node(self):
        return 'AWSLambda'