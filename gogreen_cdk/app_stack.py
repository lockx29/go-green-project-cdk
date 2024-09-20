from aws_cdk import (
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_elasticloadbalancingv2 as elbv2,
    core as cdk
)

class AppStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Auto Scaling Group for App Tier
        asg = autoscaling.AutoScalingGroup(self, "AppAsg",
            vpc=vpc,
            instance_type=ec2.InstanceType("r3.2xlarge"),  # Changed instance type to r3.2xlarge
            machine_image=ec2.AmazonLinuxImage(),
            min_capacity=3,
            max_capacity=6,
            vpc_subnets=ec2.SubnetSelection(
                subnet_group_name="AppTier"  # Ensures instances are created in AppTier subnets
            )
        )

        # Application Load Balancer for App Tier
        lb = elbv2.ApplicationLoadBalancer(self, "AppElb",
            vpc=vpc,
            internet_facing=False  # Internal ALB for app-tier
        )

        listener = lb.add_listener("Listener", port=8080)
        listener.add_targets("AppTarget", port=8080, targets=[asg])

        # Auto-scaling policies
        asg.scale_on_cpu_utilization("CpuScaling", target_utilization_percent=50)

