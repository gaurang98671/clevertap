from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_ecr as ecr,
    Duration
)
from constructs import Construct

class ECRStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, repo_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repository = ecr.Repository(    
            self, repo_name,
            repository_name=repo_name,
            removal_policy=RemovalPolicy.DESTROY,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    description="Delete untagged images after 1 day",
                    max_image_age=Duration.days(1),
                    rule_priority=1,
                    tag_status=ecr.TagStatus.UNTAGGED
                ),
                ecr.LifecycleRule(
                    description="Keep only last 10 images",
                    max_image_count=10,
                    rule_priority=2,
                    tag_status=ecr.TagStatus.ANY
                )
            ],

            image_scan_on_push=True,
            image_tag_mutability=ecr.TagMutability.MUTABLE
        )
        
        