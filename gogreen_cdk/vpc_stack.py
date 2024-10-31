from aws_cdk import aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct

class VpcStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC with 2 public and 6 private subnets
        self.vpc = ec2.Vpc(self, "GoGreenVpc",
            max_azs=2,  # Use 2 Availability Zones
            subnet_configuration=[
                ec2.SubnetConfiguration(name="PublicSubnet", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                ec2.SubnetConfiguration(name="WebTier", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24),  # Private subnet for web tier
                ec2.SubnetConfiguration(name="AppTier", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24),  # Private subnet for app tier
                ec2.SubnetConfiguration(name="DatabaseTier", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED, cidr_mask=24),  # Private isolated subnet for database
            ],
            nat_gateways=2  # 1 NAT gateway per AZ
        )