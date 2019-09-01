from modules.attack_methods.base_neo4j import BaseAttackMethod


class EC2RoleCompromise(BaseAttackMethod):
    def get_edge_types(self):
        return ['UserPublicIPAddress']

    def get_attack_difficult(self):
        return 30

    def get_attack_name(self):
        return "GrabAPIToken"

    def get_target_node(self):
        return 'EC2Instance'

    def get_source_node(self):
        return 'EC2Instance'
