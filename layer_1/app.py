#!/usr/bin/env python3
import os

import aws_cdk as cdk
from stacks.ecs_service_stack import ECSServiceStack

ENV = os.environ["CDK_ENVIRONMENT"]

VALID_ENVS = {"prod", "staging", "dev"}

if ENV not in VALID_ENVS:
    raise Exception(f"Invalid environment, expected {VALID_ENVS}, got {ENV}")

REGION = os.environ["CDK_DEFAULT_REGION"]
DEVELOPER_NAME = os.environ["DEVELOPER_NAME"].title()
PRIMARY_REGION="ap-south-1"
SECONDARY_REGIONS = ["eu-west-2"]
DEVELOPER_NAME_SUFFIX = f"_{DEVELOPER_NAME}" if DEVELOPER_NAME else ""

tags = {
    "Project": f"layer_1_infra",
    "Developer": DEVELOPER_NAME if DEVELOPER_NAME != "" else "ReleaseUser",
    "Environment": ENV
}

app = cdk.App()


for region in [PRIMARY_REGION] + SECONDARY_REGIONS:
    ecs_service_Stack = ECSServiceStack(
        app,
        f"ECSServiceStack-{region}", 
        f"VPC{DEVELOPER_NAME_SUFFIX}_{region}",
        f"backed_cluster_{DEVELOPER_NAME.lower()}_{region}",
        f"backend_service_{DEVELOPER_NAME.lower()}_{region}",
        tags=tags,
        env=cdk.Environment(region=region, account=os.environ["CDK_DEFAULT_ACCOUNT"])
    )


app.synth()
