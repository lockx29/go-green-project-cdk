#!/usr/bin/env python3

import aws_cdk as cdk

from go_green_project_cdk.go_green_vpc_stack import GoGreenProjectVpcStack


app = cdk.App()
GoGreenProjectVpcStack(app, "VpcStack", config_file="go_green_project_cdk/vpc_config.json", env=cdk.Environment(region="ap-southeast-1"))

app.synth()
