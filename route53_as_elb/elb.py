## THIS SCRIPT WAS NOT TESTED YET.

import boto3
import time

# Initialize Boto3 clients
ec2_client = boto3.client("ec2")
elbv2_client = boto3.client("elbv2")
iam_client = boto3.client("iam")

# Step 1: Create VPC (Modify this if you already have a VPC)
vpc_response = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
vpc_id = vpc_response["Vpc"]["VpcId"]
print(f"Created VPC: {vpc_id}")

ec2_client.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={"Value": True})
ec2_client.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={"Value": True})

# Step 2: Create two Subnets in different Availability Zones
subnets = []
azs = ec2_client.describe_availability_zones()["AvailabilityZones"]

for i in range(2):
    subnet_response = ec2_client.create_subnet(
        VpcId=vpc_id,
        CidrBlock=f"10.0.{i}.0/24",
        AvailabilityZone=azs[i]["ZoneName"],
    )
    subnet_id = subnet_response["Subnet"]["SubnetId"]
    subnets.append(subnet_id)
    print(f"Created Subnet: {subnet_id} in {azs[i]['ZoneName']}")

# Step 3: Create Security Group for ALB
sg_response = ec2_client.create_security_group(
    GroupName="ALB1",
    Description="Allow HTTP and HTTPS",
    VpcId=vpc_id,
)
sg_id = sg_response["GroupId"]

# Allow inbound rules for HTTP (80) and HTTPS (443)
ec2_client.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {
            "IpProtocol": "tcp",
            "FromPort": 80,
            "ToPort": 80,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
        },
        {
            "IpProtocol": "tcp",
            "FromPort": 443,
            "ToPort": 443,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
        },
    ],
)
print(f"Created Security Group: {sg_id}")

# Step 4: Create an IAM Role and Policy for SSL (Optional, needed for HTTPS termination)
role_response = iam_client.create_role(
    RoleName="ALB-SSL-Role",
    AssumeRolePolicyDocument="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "elasticloadbalancing.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }""",
)
print("Created IAM Role: ALB-SSL-Role")

iam_client.attach_role_policy(
    RoleName="ALB-SSL-Role",
    PolicyArn="arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole",
)

# # Step 5: Create Target Group for ALB
# tg_response = elbv2_client.create_target_group(
#     Name="ALB-Target-Group",
#     Protocol="HTTP",
#     Port=80,
#     VpcId=vpc_id,
#     HealthCheckProtocol="HTTP",
#     HealthCheckPort="80",
#     HealthCheckEnabled=True,
#     HealthCheckPath="/",
#     HealthCheckIntervalSeconds=30,
#     HealthCheckTimeoutSeconds=5,
#     HealthyThresholdCount=5,
#     UnhealthyThresholdCount=2,
#     TargetType="instance",
# )
# target_group_arn = tg_response["TargetGroups"][0]["TargetGroupArn"]
# print(f"Created Target Group: {target_group_arn}")

# # Step 6: Register EC2 Instances with Target Group (Modify instance IDs)
# instance_ids = [
#     "i-0123456789abcdef0",
#     "i-0abcdef1234567890",
# ]  # Replace with actual instance IDs
# elbv2_client.register_targets(
#     TargetGroupArn=target_group_arn,
#     Targets=[{"Id": instance_id} for instance_id in instance_ids],
# )
# print(f"Registered Instances to Target Group: {instance_ids}")


# Step 7: Create Application Load Balancer
alb_response = elbv2_client.create_load_balancer(
    Name="ALB1",
    Subnets=subnets,
    SecurityGroups=[sg_id],
    Scheme="internet-facing", # Options: internet-facing, internal
    Type="application",
    IpAddressType="ipv4", # Options: ipv4, dualstack
)
alb_arn = alb_response["LoadBalancers"][0]["LoadBalancerArn"]
alb_dns = alb_response["LoadBalancers"][0]["DNSName"]
print(f"Created ALB: {alb_arn}, DNS: {alb_dns}")

# Step 8: Create HTTP Listener (Specify the Target Group)
http_listener_response = elbv2_client.create_listener(
    LoadBalancerArn=alb_arn,
    Protocol="HTTP",
    Port=80,
    DefaultActions=[{"Type": "forward", "TargetGroupArn": target_group_arn}],
)
http_listener_arn = http_listener_response["Listeners"][0]["ListenerArn"]
print(f"Created HTTP Listener: {http_listener_arn}")

# Step 9: Create HTTPS Listener (Requires an SSL Certificate)
# Replace ARN with your actual ACM Certificate ARN
ssl_certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/your-ssl-cert-arn"
https_listener_response = elbv2_client.create_listener(
    LoadBalancerArn=alb_arn,
    Protocol="HTTPS",
    Port=443,
    SslPolicy="ELBSecurityPolicy-2016-08",
    Certificates=[{"CertificateArn": ssl_certificate_arn}],
    DefaultActions=[{"Type": "forward", "TargetGroupArn": target_group_arn}],
)
https_listener_arn = https_listener_response["Listeners"][0]["ListenerArn"]
print(f"Created HTTPS Listener: {https_listener_arn}")

# Step 10: Wait until ALB is active
while True:
    alb_status = elbv2_client.describe_load_balancers(LoadBalancerArns=[alb_arn])
    state = alb_status["LoadBalancers"][0]["State"]["Code"]
    if state == "active":
        break
    print(f"Waiting for ALB to become active... Current state: {state}")
    time.sleep(10)

print("ALB is now active and ready to use!")

# Step 11: Output Load Balancer DNS
print(f"ALB DNS Name: {alb_dns}")

