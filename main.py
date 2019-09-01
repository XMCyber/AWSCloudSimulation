from modules import simple_storage
from modules.attack_methods.aws.access_key_usage import AccessKeyUsage
from modules.attack_methods.aws.ec2_ssm import EC2SSMRunCommand
from modules.attack_methods.aws.lambda_function_role_usage import LambdaRoleUsage
from modules.attack_methods.aws.lambda_modify import LambdaModifyCode
from modules.attack_methods.aws.storage__modify import EC2RemountStorage
from modules.info_gather.aws.cloudtrail import CloudtrailGather
from modules.info_gather.aws.ec2 import Ec2Gather
from modules.info_gather.aws.iam import IamGather
from modules.info_gather.aws.lambda_function import LambdaGather
from modules.info_gather.aws.s3 import S3Gather
from modules.node_and_relationships.aws.role_to_ec2 import RoleToEC2
from modules.node_and_relationships.aws.role_to_lambda import RoleToLambda
from modules.graph_exporter import csv, neo4j
from modules.node_and_relationships.aws.access_key_to_user import AccessKeyToUser
from modules.node_and_relationships.aws.ec2_to_publicip import EC2ToPublicIP
from modules.node_and_relationships.aws.ec2_to_role import EC2ToRole
from modules.node_and_relationships.aws.lamda_to_role import LambdaToRole
from modules.node_and_relationships.aws.role_to_ssm_powershell import RoleToSSM

Ec2Gather(simple_storage).init()
IamGather(simple_storage).init()
LambdaGather(simple_storage).init()
S3Gather(simple_storage).init()
CloudtrailGather(simple_storage).init()

print("Finish Gather")

EC2ToPublicIP(simple_storage).init()
AccessKeyToUser(simple_storage).init()
LambdaToRole(simple_storage).init()
EC2ToRole(simple_storage).init()

RoleToLambda(simple_storage).init()
RoleToEC2(simple_storage).init()
RoleToSSM(simple_storage).init()

#csv.export()
neo4j.export()

LambdaModifyCode().calc_query()
EC2SSMRunCommand().calc_query()
AccessKeyUsage().calc_query()
LambdaRoleUsage().calc_query()
EC2RemountStorage().calc_query()
simple_storage.close_dbs()
