from aws_cdk import (
    aws_rds as rds,
    aws_ec2 as ec2,
    core as cdk
)

class DatabaseStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # RDS Instance
        db_instance = rds.DatabaseInstance(self, "RdsInstance",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_13),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
            vpc=vpc,
            multi_az=True,
            allocated_storage=100,
            storage_encrypted=True,
            backup_retention=cdk.Duration.days(7),
            deletion_protection=False,
            publicly_accessible=False
        )
