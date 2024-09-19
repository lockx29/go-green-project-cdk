from aws_cdk import (
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as autoscaling,
    aws_ecs as ecs,
    core as cdk
)

class WebStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Auto Scaling Group for Web Tier
        asg = autoscaling.AutoScalingGroup(self, "WebAsg",
            vpc=vpc,
            instance_type=ec2.InstanceType("t2.large"),
            machine_image=ec2.AmazonLinuxImage(),
            min_capacity=2,
            max_capacity=6
        )

        # Create Elastic Load Balancer
        lb = elbv2.ApplicationLoadBalancer(self, "WebElb",
            vpc=vpc,
            internet_facing=True
        )

        listener = lb.add_listener("Listener", port=80)
        listener.add_targets("WebTarget", port=80, targets=[asg])

        # Auto-scaling policies
        asg.scale_on_cpu_utilization("CpuScaling", target_utilization_percent=50)
