from modules.attack_methods.base_neo4j import BaseAttackMethod


class EC2SSMRunCommand(BaseAttackMethod):
    def get_edge_types(self):
        return ['ssm:SendCommand', 'ec2:AssociateIamInstanceProfile', 'ec2:StopInstances', 'ec2:StartInstances', 'ec2:DescribeInstances']

    def get_attack_difficult(self):
        return 10

    def get_attack_name(self):
        return "SSMRunCommand"

    def get_target_node(self):
        return 'EC2Instance'

    def get_source_node(self):
        return 'AWSRole'
