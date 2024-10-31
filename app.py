#!/usr/bin/env python3
import aws_cdk as cdk
from gogreen_cdk.vpc_stack import VpcStack
from gogreen_cdk.web_stack import WebStack
from gogreen_cdk.app_stack import AppStack
from gogreen_cdk.database_stack import DatabaseStack

app = cdk.App()

# Create VPC stack
vpc_stack = VpcStack(app, "VpcStack", env=cdk.Environment(region="us-east-1"))

# Create Web Tier stack
web_stack = WebStack(app, "WebStack", vpc=vpc_stack.vpc, env=cdk.Environment(region="us-east-1"))

# Create App Tier stack
app_stack = AppStack(app, "AppStack", vpc=vpc_stack.vpc, env=cdk.Environment(region="us-east-1"))

# Create Database Tier stack
database_stack = DatabaseStack(app, "DatabaseStack", vpc=vpc_stack.vpc, env=cdk.Environment(region="us-east-1"))

app.synth()

