from modules import simple_storage
from modules.api_runner.aws import run_single_region
from modules.node_and_relationships.aws.nodes import BaseRoleNode, BaseLambdaNode
from modules.node_and_relationships.node_and_relationships_runner import NodesAndRelationshipsBase


class RoleToLambda(NodesAndRelationshipsBase):

    def get_relation_name(self):
        return "RoleToLambda"

    @staticmethod
    def should_cache():
        return True

    def init(self):
        all_lambda_functions = simple_storage.all_records('lambda_function')
        all_lambda_functions_arn = set([])
        for lambda_function in all_lambda_functions:
            all_lambda_functions_arn.add(lambda_function['FunctionArn'])

        all_users = simple_storage.all_records('iam_gatherusers')
        all_users.extend(simple_storage.all_records('iam_gatherroles'))

        if len(all_lambda_functions_arn) == 0:
            return

        for user in all_users:

            simulation_params = {
                'PolicySourceArn': user['Arn'],
                'ActionNames': ['lambda:GetFunction', 'lambda:UpdateFunctionCode'],
                'ResourceArns': list(all_lambda_functions_arn),
                'ContextEntries': [{
                    'ContextKeyName': 'aws:multifactorauthpresent',
                    'ContextKeyType': 'boolean',
                    'ContextKeyValues': ['true']
                }]
            }
            all_simulations = run_single_region('iam', 'simulate_principal_policy', simulation_params)
            for simulation_data in all_simulations["EvaluationResults"]:
                if simulation_data["EvalDecision"] == "allowed":
                    lambda_node = BaseLambdaNode(simulation_data['EvalResourceName'])
                    role_node = BaseRoleNode(user['Arn'])
                    role_node.relate(self.storage, lambda_node, simulation_data['EvalActionName'])