from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
)
from constructs import Construct

class EcsClusterStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, cluster_name:str, vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        
        self.cluster = ecs.Cluster(
            self,
            cluster_name,
            cluster_name=cluster_name,
            vpc=vpc
        )
