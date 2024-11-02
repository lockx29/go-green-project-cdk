from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    Stack,
    Duration
)
from constructs import Construct

class DatabaseStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create RDS MySQL Instance in DatabaseTier
        db_instance = rds.DatabaseInstance(self, "GoGreenSQLInstance",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_28  # MySQL version 8.0
            ),
            instance_type=ec2.InstanceType("db.t2.micro"),  # Set instance type to db.m5.2xlarge during actual implementation
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_group_name="DatabaseTier"  # Ensures the RDS instance is created in DatabaseTier subnets
            ),
            allocated_storage=5500,  # Allocating 5.5 TB of storage (in GB)
            multi_az=True,  # Enable Multi-AZ deployment for high availability
            storage_encrypted=True,  # Encrypt storage
            backup_retention=Duration.days(7),  # Retain backups for 7 days
            deletion_protection=True,  # Enable deletion protection
            database_name="GoGreenAppDB",
            credentials=rds.Credentials.from_generated_secret("admin"),  # Automatically generate and store admin credentials
            publicly_accessible=False  # Make RDS instance private
        )
