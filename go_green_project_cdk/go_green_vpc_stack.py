import json
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput
)
from constructs import Construct

class GoGreenProjectVpcStack(Stack):

    def __init__(self, scope: Construct, id: str, config_file: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Load the configuration from the file
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        vpc_name = config.get("vpc_name", "DefaultVPC")
        nat_name = config.get("nat_name", "DefaultNAT")
        public_subnet_names = config.get("public_subnet_names", [])
        app_private_subnet_names = config.get("app_private_subnet_names", [])
        db_private_subnet_names = config.get("db_private_subnet_names", [])
        
        # Ensure there are enough subnet names in the config
        if len(public_subnet_names) != 2:
            raise ValueError("Config must contain exactly two public subnet names.")
        if len(app_private_subnet_names) != 2:
            raise ValueError("Config must contain exactly two application private subnet names.")
        if len(db_private_subnet_names) != 2:
            raise ValueError("Config must contain exactly two database private subnet names.")
        
        # Create a VPC
        vpc = ec2.Vpc(
            self, "GoGreen",
            vpc_name=vpc_name,
            max_azs=2,  # Limit to 2 availability zones
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=public_subnet_names[0],
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name=public_subnet_names[1],
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name=app_private_subnet_names[0],
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name=app_private_subnet_names[1],
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name=db_private_subnet_names[0],
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name=db_private_subnet_names[1],
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ],
            nat_gateways=1  # Use one NAT Gateway for private subnets
        )

