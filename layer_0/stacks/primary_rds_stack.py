from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
)
from constructs import Construct

class PrimaryRDSStack(Stack):
    def __init__(self, scope: Construct, construct_id, vpc, database_name:str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.primary_db = rds.DatabaseInstance(
            self,
            "PrimaryPostgres",
            instance_identifier=database_name,
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_17_4
            ),
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.SMALL,
            ),
            multi_az=True,
            allocated_storage=50,
            publicly_accessible=False,
            deletion_protection=False,
        )
