#!/usr/bin/env python

import os
import aws_cdk as cdk
from stacks.vpc_stack import VPCStack
from stacks.ecr_stack import ECRStack
from stacks.ecs_stack import EcsClusterStack
from stacks.primary_rds_stack import PrimaryRDSStack
from stacks.secondary_rds_stack import SecondaryRDSStack
from stacks.policies.iam_stack import IAMStack

ENV = os.environ["CDK_ENVIRONMENT"]

VALID_ENVS = {"prod", "staging", "dev"}

if ENV not in VALID_ENVS:
    raise Exception(f"Invalid environment, expected {VALID_ENVS}, got {ENV}")

REGION = os.environ["CDK_REGION"]
DEVELOPER_NAME = os.environ["DEVELOPER_NAME"].title()
PRIMARY_REGION="ap-south-1"
SECONDARY_REGIONS = ["eu-west-2"]
DEVELOPER_NAME_SUFFIX = f"_{DEVELOPER_NAME}" if DEVELOPER_NAME else ""

tags = {
    "Project": f"layer_0_infra",
    "Developer": DEVELOPER_NAME if DEVELOPER_NAME != "" else "ReleaseUser",
    "Environment": ENV
}

app = cdk.App()
store = {}

# Below stuff is common for all regions
for region in [PRIMARY_REGION] + SECONDARY_REGIONS:
    vpc_stack = VPCStack(
        app, 
        f"VPCStack-{region}",
        f"VPC{DEVELOPER_NAME_SUFFIX}_{region}",
        tags=tags,
        env=cdk.Environment(region=region),
        cross_region_references=True
    )
    
    ecr_repo_stack = ECRStack(
        app,
        f"ECRStack-{region}",
        f"backend_service{DEVELOPER_NAME_SUFFIX.lower()}_{region}",
        tags=tags,
        env=cdk.Environment(region=region)
    )

    ecs_cluster_stack = EcsClusterStack(
        app,
        f"EcsClusterStack-{region}",
        f"backed_cluster{DEVELOPER_NAME_SUFFIX.lower()}_{region}",
        vpc_stack.vpc,
        tags=tags,
        env=cdk.Environment(region=region)
    )

    store[region] = {
        "vpc": vpc_stack,
        "ecr": ecr_repo_stack,
        "ecs": ecs_cluster_stack
    }


primary_rds = PrimaryRDSStack(
    app,
    f"PrimaryRDSStack-{PRIMARY_REGION}",
    store[PRIMARY_REGION]["vpc"].vpc,
    f"backend-writer-instance-{PRIMARY_REGION}",
    tags=tags,
    env=cdk.Environment(region=PRIMARY_REGION),
    cross_region_references=True
)

print(f"Creating writer instance in {PRIMARY_REGION}")

for region in SECONDARY_REGIONS:

    print(f"Creating reader instance in {region}")
    secondary_rds = SecondaryRDSStack(
        app,
        f"SecondaryRDSStack-{region}",
        primary_rds.primary_db,
        store[region]["vpc"].vpc,
        tags=tags,
        env=cdk.Environment(region=region)
    )


iam_stack = IAMStack(app, "IAMStack", ENV, tags=tags)


app.synth()