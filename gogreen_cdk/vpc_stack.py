from aws_cdk import (
    aws_ec2 as ec2,
    core as cdk
)

class VpcStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC with 2 public and 6 private subnets
        self.vpc = ec2.Vpc(self, "GoGreenVpc",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="PublicSubnet", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                ec2.SubnetConfiguration(name="PrivateSubnet", subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT, cidr_mask=24),
            ],
            nat_gateways=1
        )
