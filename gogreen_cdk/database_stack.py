from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core as cdk
)

class DatabaseStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create RDS MySQL Instance in DatabaseTier
        db_instance = rds.DatabaseInstance(self, "MySQLInstance",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_28  # MySQL version 8.0
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.MEMORY5, ec2.InstanceSize.XLARGE2  # r5.2xlarge instance (8 vCPUs, 32 GB RAM)
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_group_name="DatabaseTier"  # Ensures the RDS instance is created in DatabaseTier subnets
            ),
            allocated_storage=5500,  # Allocating 5.5 TB of storage (in GB)
            multi_az=True,  # Enable Multi-AZ deployment for high availability
            storage_encrypted=True,  # Encrypt storage
            backup_retention=cdk.Duration.days(7),  # Retain backups for 7 days
            deletion_protection=True,  # Enable deletion protection
            database_name="MyAppDB",
            credentials=rds.Credentials.from_generated_secret("admin"),  # Automatically generate and store admin credentials
            publicly_accessible=False  # Make RDS instance private
        )

