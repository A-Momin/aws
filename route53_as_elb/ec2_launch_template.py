################################################################################
############################## Provided by ChatGPT #############################
################################################################################


# Initialize EC2 client
client = boto3.client("ec2", region_name="us-east-1")  # Change region as needed

# Define Launch Template parameters
launch_template_name = "MyLT"
ami_id = "ami-085ad6ae776d8f09c"  # Replace with actual AMI ID
instance_type = "t2.micro"
key_name = "AMominNJ"  # Replace with your Key Pair name
security_group_ids = [web1_sg]  # Replace with actual security group IDs
# iam_instance_profile = "arn:aws:iam::123456789012:instance-profile/MyInstanceProfile"  # Replace with actual IAM Role
# subnet_id = "subnet-0123456789abcdef0"  # Replace with actual Subnet ID

# User Data (Base64 Encoded)
user_data_script = """#!/bin/bash

# Update the system and install Apache
yum update -y
yum install -y httpd

# Start and enable Apache to run on boot
systemctl start httpd
systemctl enable httpd

# Fetch the latest token for accessing EC2 instance metadata
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

# Fetch the instance ID
INSTANCEID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id -H "X-aws-ec2-metadata-token: $TOKEN")

# Create or overwrite `index.html` with the instance ID information
echo "<center><h1>This instance has the ID: $INSTANCEID </h1></center>" > /var/www/html/index.html

# Ensure httpd can read the `index.html` file and its directory
chown apache:apache /var/www/html/index.html
chmod 755 /var/www/html
chmod 644 /var/www/html/index.html

# Restart Apache to apply changes
systemctl restart httpd
"""
user_data_encoded = base64.b64encode(user_data_script.encode("utf-8")).decode("utf-8")

# Define Block Device Mappings
block_device_mappings = [
    {
        "DeviceName": "/dev/xvda",
        "Ebs": {
            "VolumeSize": 20,  # 20 GB Root Volume
            "VolumeType": "gp3",
            "DeleteOnTermination": True,
            "Encrypted": True,
        },
    },
    {
        "DeviceName": "/dev/xvdb",
        "Ebs": {
            "VolumeSize": 50,  # Additional 50 GB Volume
            "VolumeType": "gp3",
            "DeleteOnTermination": False,
            "Encrypted": False,
        },
    },
]

# Create Launch Template
response = client.create_launch_template(
    LaunchTemplateName=launch_template_name,
    VersionDescription="Initial Version",
    LaunchTemplateData={
        "ImageId": ami_id,
        "InstanceType": instance_type,
        "KeyName": key_name,
        "SecurityGroupIds": security_group_ids,
        "IamInstanceProfile": {"Arn": iam_instance_profile},
        "UserData": user_data_encoded,
        "BlockDeviceMappings": block_device_mappings,
        "NetworkInterfaces": [
            {
                "SubnetId": subnet_id,
                "DeviceIndex": 0,
                "AssociatePublicIpAddress": True,
                "Groups": security_group_ids,
            }
        ],
        "TagSpecifications": [
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Environment", "Value": "Production"}],
            }
        ],
        "Monitoring": {"Enabled": True},  # Enable detailed monitoring
        "DisableApiTermination": False,  # Allow instance termination
        "InstanceInitiatedShutdownBehavior": "stop",  # Stop instance on shutdown
    },
)

# Extract Launch Template ID & ARN
launch_template_id = response["LaunchTemplate"]["LaunchTemplateId"]
launch_template_arn = response["LaunchTemplate"]["LaunchTemplateArn"]

print("Launch Template Created Successfully!")
print(f"Launch Template ID: {launch_template_id}")
print(f"Launch Template ARN: {launch_template_arn}")


############################## Provided by Copilot ##############################

import boto3

# Initialize a session using Amazon EC2
session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='YOUR_REGION'
)

# Create an ELB client
elbv2 = session.client('elbv2')

# Create a target group
response = elbv2.create_target_group(
    Name='my-target-group',
    Protocol='HTTP',
    Port=80,
    VpcId='vpc-12345678',
    HealthCheckProtocol='HTTP',
    HealthCheckPort='traffic-port',
    HealthCheckEnabled=True,
    HealthCheckPath='/',
    HealthCheckIntervalSeconds=30,
    HealthCheckTimeoutSeconds=5,
    HealthyThresholdCount=5,
    UnhealthyThresholdCount=2,
    Matcher={
        'HttpCode': '200'
    },
    TargetType='instance',
    Tags=[
        {
            'Key': 'Name',
            'Value': 'my-target-group'
        }
    ]
)

# Print the response
print(response)
