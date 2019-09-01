from modules.node_and_relationships.base_node import BaseNode


class BaseEC2Node(BaseNode):
    def __init__(self, instance_id):
        self.instance_id = instance_id

    def get_id(self):
        return self.instance_id

    def get_labels(self):
        return 'EC2Instance'

    def get_node_type(self):
        return 'ec2_instance'


class BaseLambdaNode(BaseNode):
    def __init__(self, lambda_arn):
        self.lambda_arn = lambda_arn

    def get_labels(self):
        return 'AWSLambda'

    def get_id(self):
        return self.lambda_arn

    def get_node_type(self):
        return 'lambda_function'


class BaseRoleNode(BaseNode):
    def __init__(self, role_arn):
        self.role_arn = role_arn

    def get_labels(self):
        return 'AWSRole'

    def get_id(self):
        return self.role_arn

    def get_node_type(self):
        return 'iam_role'


class BaseIamAccessKey(BaseNode):
    def __init__(self, access_key_id):
        self.access_key_id = access_key_id

    def get_labels(self):
        return 'IAMAccessKey'

    def get_id(self):
        return self.access_key_id

    def get_node_type(self):
        return 'iam_access_key'


class BasePublicIP(BaseNode):
    def __init__(self, ip_addr):
        self.ip_addr = ip_addr

    def get_labels(self):
        return 'VPCIpAddress'

    def get_id(self):
        return self.ip_addr

    def get_node_type(self):
        return 'public_ip_addr'

