from modules import simple_storage
from modules.api_runner.aws import run_single_region
from modules.node_and_relationships.aws.nodes import BaseEC2Node, BaseRoleNode
from modules.node_and_relationships.node_and_relationships_runner import NodesAndRelationshipsBase


class RoleToEC2(NodesAndRelationshipsBase):

    def get_relation_name(self):
        return "RoleToEC2"

    @staticmethod
    def should_cache():
        return True

    def init(self):
        all_instances = simple_storage.all_records('ec2_gather')
        all_instances.append({'InstanceId': "ALL-INSTANCES"})
        all_instances_arn = set([])
        basic_arn = 'arn:aws:ec2:*:*:instance/'
        for instance in all_instances:
            all_instances_arn.add(basic_arn + instance['InstanceId'])

        all_users = simple_storage.all_records('iam_gatherusers')
        all_users.extend(simple_storage.all_records('iam_gatherroles'))
        ''''ec2:AssociateIamInstanceProfile',
                                'ec2:DetachVolume',
                                'ec2:AttachVolume','''
        if len(all_instances_arn) == 0:
            return

        for user in all_users:
            simulation_params = {
                'PolicySourceArn': user['Arn'],
                'ActionNames': [
                    #'ec2:AssociateIamInstanceProfile'
                    #'ec2:StartInstances',
                    #'ec2:StopInstances'
                    'ec2:AttachVolume',
                    'ec2:DetachVolume'
                ],
                'ResourceArns': list(all_instances_arn),
                'ContextEntries': [{
                    'ContextKeyName': 'aws:multifactorauthpresent',
                    'ContextKeyType': 'boolean',
                    'ContextKeyValues': ['true']
                }]
            }
            all_simulations = run_single_region('iam', 'simulate_principal_policy', simulation_params)
            #all_simulations = {"EvaluationResults": []}
            for simulation_data in all_simulations["EvaluationResults"]:
                if simulation_data["EvalDecision"] == "allowed":
                    ec2_node = BaseEC2Node(simulation_data['EvalResourceName'][len(basic_arn):])
                    role_node = BaseRoleNode(user['Arn'])
                    role_node.relate(self.storage, ec2_node, simulation_data['EvalActionName'])
            simulation_params = {
                'PolicySourceArn': user['Arn'],
                'ActionNames': [
                    #'ec2:AssociateIamInstanceProfile'
                    'ec2:StartInstances',
                    'ec2:StopInstances'
                    #'ec2:AttachVolume'
                                ],
                'ResourceArns': list(all_instances_arn),
                'ContextEntries': [{
                    'ContextKeyName': 'aws:multifactorauthpresent',
                    'ContextKeyType': 'boolean',
                    'ContextKeyValues': ['true']
                }]
            }
            all_simulations = run_single_region('iam', 'simulate_principal_policy', simulation_params)
            #all_simulations = {"EvaluationResults": []}
            for simulation_data in all_simulations["EvaluationResults"]:
                if simulation_data["EvalDecision"] == "allowed":
                    ec2_node = BaseEC2Node(simulation_data['EvalResourceName'][len(basic_arn):])
                    role_node = BaseRoleNode(user['Arn'])
                    role_node.relate(self.storage, ec2_node, simulation_data['EvalActionName'])

            simulation_params = {
                'PolicySourceArn': user['Arn'],
                'ActionNames': [
                    'ec2:AssociateIamInstanceProfile'
                    #'ec2:StartInstances',
                    #'ec2:StopInstances'
                    #'ec2:AttachVolume'
                ],
                'ResourceArns': list(all_instances_arn),
                'ContextEntries': [{
                    'ContextKeyName': 'aws:multifactorauthpresent',
                    'ContextKeyType': 'boolean',
                    'ContextKeyValues': ['true']
                }]
            }
            all_simulations = run_single_region('iam', 'simulate_principal_policy', simulation_params)
            #all_simulations = {"EvaluationResults": []}
            for simulation_data in all_simulations["EvaluationResults"]:
                if simulation_data["EvalDecision"] == "allowed":
                    ec2_node = BaseEC2Node(simulation_data['EvalResourceName'][len(basic_arn):])
                    role_node = BaseRoleNode(user['Arn'])
                    role_node.relate(self.storage, ec2_node, simulation_data['EvalActionName'])


            simulation_params = {
                        'PolicySourceArn': user['Arn'],
                        'ActionNames': [
                                        'ec2:DescribeInstances',
                                        'ec2:ModifyInstanceAttribute',
                                        'ec2:CopySnapshot',
                                        'ec2:RunInstances'
                                        ],
                        'ContextEntries': [{
                            'ContextKeyName': 'aws:multifactorauthpresent',
                            'ContextKeyType': 'boolean',
                            'ContextKeyValues': ['true']
                        }]
                        }
            all_simulations = run_single_region('iam', 'simulate_principal_policy', simulation_params)
            for simulation_data in all_simulations["EvaluationResults"]:
                if simulation_data["EvalDecision"] == "allowed":
                    for instance in all_instances:
                        ec2_node = BaseEC2Node(instance['InstanceId'])
                        role_node = BaseRoleNode(user['Arn'])
                        role_node.relate(self.storage, ec2_node, simulation_data['EvalActionName'])