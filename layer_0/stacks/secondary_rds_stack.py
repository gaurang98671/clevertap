from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
)
from constructs import Construct

class SecondaryRDSStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, source_database_instance: str, vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        rds.DatabaseInstanceReadReplica(
            self,
            "PostgresReadReplica",
            source_database_instance=source_database_instance,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MEDIUM,
            ),
            vpc=vpc,
            publicly_accessible=False,
        )
