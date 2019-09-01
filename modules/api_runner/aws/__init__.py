import boto3
from modules import config
REGIONS = config.config['AWS']['SUPPORTED_REGIONS']

boto3.setup_default_session(profile_name=config.config["AWS"]["PROFILE"])


def run_single_region(service_name, service_function, arguments):
    service_obj = boto3.client(service_name)
    return getattr(service_obj, service_function)(**arguments)


def run_api_cross_region(service_name, service_function, arguments):
    region_output_map = {}
    for region in REGIONS:
        service_obj = boto3.client(service_name, region_name=region)
        region_output_map[region] = getattr(service_obj, service_function)(**arguments)
    return region_output_map


def run_api_paginated_cross_region(service_name, service_function, arguments):
    region_output_map = {}
    for region in REGIONS:
        service_obj = boto3.client(service_name, region_name=region)
        paginator = service_obj.get_paginator(service_function)
        region_output_map[region] = paginator.paginate()
    return region_output_map

