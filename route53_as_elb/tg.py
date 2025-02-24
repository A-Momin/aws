import boto3

# Initialize AWS client for Elastic Load Balancing v2 (ELBv2)
client = boto3.client("elbv2", region_name="us-east-1")  # Change region as needed

# Define the target group parameters
target_group_name = "TG1"
vpc_id = "vpc-0123456789abcdef0"  # Replace with your actual VPC ID

response = client.create_target_group(
    Name=target_group_name,
    Protocol="HTTP",  # Options: HTTP, HTTPS, TCP, TLS, UDP, TCP_UDP, GENEVE
    Port=80,  # Port on which the target is listening
    VpcId=vpc_id,
    HealthCheckProtocol="HTTP",  # Options: HTTP, HTTPS, TCP, TLS
    HealthCheckPort="traffic-port",  # Use "traffic-port" to match the listener port
    HealthCheckEnabled=True,  # Enable health checks
    HealthCheckPath="/",  # Path for health check requests
    HealthCheckIntervalSeconds=30,  # Interval in seconds between health checks
    HealthCheckTimeoutSeconds=5,  # Timeout before considering the check as failed
    HealthyThresholdCount=3,  # Number of successful checks to consider healthy
    UnhealthyThresholdCount=2,  # Number of failed checks to consider unhealthy
    Matcher={"HttpCode": "200-299"},  # HTTP response code for a successful health check
    TargetType="instance",  # Options: instance, ip, lambda, alb
    Tags=[{"Key": "Environment", "Value": "Production"}],  # Optional tags
)

# Extract the Target Group ARN
target_group_arn = response["TargetGroups"][0]["TargetGroupArn"]
print(f"Target Group created: {target_group_arn}")

## We will be attaching the Target Group to the Auto Scaling Group in the next step.

# # Attach targets to the target group (optional step)
# targets = [
#     {"Id": "i-0abcd1234efgh5678", "Port": 80},  # Replace with actual instance ID
# ]

# response = client.register_targets(
#     TargetGroupArn=target_group_arn,
#     Targets=targets,
# )

# print("Targets registered successfully!")

# # Wait for targets to become healthy
# waiter = client.get_waiter("target_in_service")
# waiter.wait(TargetGroupArn=target_group_arn)
# print("Targets are now healthy!")
