import boto3

# Initialize clients
ec2_client = boto3.client("ec2", region_name="us-east-1")
autoscaling_client = boto3.client("autoscaling", region_name="us-east-1")
elbv2_client = boto3.client("elbv2", region_name="us-east-1")

# Define parameters
launch_template_name = "my-launch-template"
asg_name = "my-auto-scaling-group"
vpc_id = "vpc-xxxxxxxx"  # Replace with your VPC ID
subnets = ["subnet-xxxxxxxx", "subnet-yyyyyyyy"]  # Replace with valid subnet IDs
instance_type = "t3.micro"
ami_id = "ami-xxxxxxxx"  # Replace with your AMI ID
key_name = "my-key-pair"  # Replace with your SSH key name
security_groups = ["sg-xxxxxxxx"]  # Replace with valid security group IDs

# Step 1: Create Launch Template
launch_template_response = ec2_client.create_launch_template(
    LaunchTemplateName=launch_template_name,
    VersionDescription="Initial version",
    LaunchTemplateData={
        "ImageId": ami_id,
        "InstanceType": instance_type,
        "KeyName": key_name,
        "SecurityGroupIds": security_groups,
        "UserData": "IyEvYmluL2Jhc2ggZWNobyAiSGVsbG8gd29ybGQi",
        "TagSpecifications": [
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Environment", "Value": "Production"}],
            }
        ],
        "Monitoring": {"Enabled": True},
        "InstanceInitiatedShutdownBehavior": "terminate",
    },
)
launch_template_id = launch_template_response["LaunchTemplate"]["LaunchTemplateId"]
print(f"Launch Template Created: {launch_template_id}")

# Step 2: Retrieve Target Group ARN of Existing ALB
load_balancer_arn = "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-load-balancer/abcdefghij"  # Replace with your ALB ARN
target_group_name = "my-target-group"  # Replace with your Target Group name

# Fetch the existing target group ARN
target_groups_response = elbv2_client.describe_target_groups(Names=[target_group_name])
target_group_arn = target_groups_response["TargetGroups"][0]["TargetGroupArn"]
print(f"Target Group ARN Found: {target_group_arn}")

# Step 3: Create Auto Scaling Group & Attach to ALB
asg_response = autoscaling_client.create_auto_scaling_group(
    AutoScalingGroupName=asg_name,
    LaunchTemplate={"LaunchTemplateId": launch_template_id, "Version": "$Latest"},
    MinSize=1,
    MaxSize=5,
    DesiredCapacity=2,
    VPCZoneIdentifier=",".join(subnets),
    HealthCheckType="ELB",
    HealthCheckGracePeriod=300,
    Tags=[{"Key": "Environment", "Value": "Production", "PropagateAtLaunch": True}],
    NewInstancesProtectedFromScaleIn=True,
    DefaultCooldown=300,
    AvailabilityZones=["us-east-1a", "us-east-1b"],
    TerminationPolicies=["Default"],
    TargetGroupARNs=[target_group_arn],  # Attach ASG to ALB Target Group
    InstanceMaintenancePolicy={"MinHealthyPercentage": 50, "MaxHealthyPercentage": 100},
)
print(f"Auto Scaling Group Created and Attached to ALB: {asg_name}")

# Step 4: Attach Scaling Policies
scaling_policy_response = autoscaling_client.put_scaling_policy(
    AutoScalingGroupName=asg_name,
    PolicyName="ScaleUpPolicy",
    PolicyType="TargetTrackingScaling",
    TargetTrackingConfiguration={
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "ASGAverageCPUUtilization"
        },
        "TargetValue": 50.0,
        "ScaleOutCooldown": 300,
        "ScaleInCooldown": 300,
    },
)
print("Scaling Policy Created:", scaling_policy_response["PolicyARN"])

# Step 5: Attach Notifications (Optional)
autoscaling_client.put_notification_configuration(
    AutoScalingGroupName=asg_name,
    TopicARN="arn:aws:sns:us-east-1:123456789012:MySNSTopic",
    NotificationTypes=[
        "autoscaling:EC2_INSTANCE_LAUNCH",
        "autoscaling:EC2_INSTANCE_TERMINATE",
    ],
)
print("Notification Configurations Set")

# Step 6: Verify Auto Scaling Group Status
asg_status = autoscaling_client.describe_auto_scaling_groups(
    AutoScalingGroupNames=[asg_name]
)
print("Auto Scaling Group Details:", asg_status)
