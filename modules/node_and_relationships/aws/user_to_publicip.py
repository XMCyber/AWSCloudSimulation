from modules import simple_storage
from modules.node_and_relationships.aws.nodes import BaseRoleNode, BasePublicIP
from modules.node_and_relationships.node_and_relationships_runner import NodesAndRelationshipsBase


class UserToPublicIP(NodesAndRelationshipsBase):
    def get_relation_name(self):
        return "UserToPublicIP"

    @staticmethod
    def should_cache():
        return False

    def init(self):
        all_users_to_ip = simple_storage.all_records('user_to_ip')

        all_users = simple_storage.all_records('users')
        all_roles = simple_storage.all_records('roles')

        name_to_arn = {}
        for user in all_users:
            name_to_arn[user['UserName']] = user['Arn']
        for role in all_roles:
            name_to_arn[role['RoleName']] = role['Arn']

        for user in all_users_to_ip:
            if user['username'] not in name_to_arn:
                continue
            user_node = BaseRoleNode(name_to_arn[user['username']])
            for ip in user['ips']:
                ip_node = BasePublicIP(ip)
                ip_node.relate(user_node, "UserPublicIPAddress")