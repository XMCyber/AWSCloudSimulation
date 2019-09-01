from modules.attack_methods.base_neo4j import BaseAttackMethod


class EC2RemountStorage(BaseAttackMethod):
    def get_edge_types(self):
        return ['ec2:RunInstances', 'ec2:DetachVolume', 'ec2:AttachVolume', 'ec2:StopInstances', 'ec2:StartInstances', 'ec2:DescribeInstances']

    def get_attack_difficult(self):
        return 20

    def get_attack_name(self):
        return "EC2StorageModify"

    def get_target_node(self):
        return 'EC2Instance'

    def get_source_node(self):
        return 'AWSRole'
