import boto3
import time
import json

# Initialize the CloudFormation client
cloudformation = boto3.client("cloudformation", region_name="us-east-1")  # Change as needed

# Read CloudFormation template from a file
with open("/Users/am/mydocs/Software_Development/Web_Development/aws/auto_scaling_and_load_balancing/alb-cf-template.yml", "r") as file:
    template_body = file.read()

# Define stack name
stack_name = "secure-listner-lab"

# Define CloudFormation parameters
parameters = [
    {"ParameterKey": "VPCId", "ParameterValue": "vpc-03617a8a518caa526"},  # Replace with actual VPC ID
    {"ParameterKey": "SubnetIdOne", "ParameterValue": "subnet-0a972b05a5b162feb"},  # default-subnet-a
    {"ParameterKey": "SubnetIdTwo", "ParameterValue": "subnet-0ca765b361e4cb186"},  # default-subnet-c
    {"ParameterKey": "ImageId", "ParameterValue": "ami-053a45fff0a704a47"},  # Replace with valid AMI ID
    {"ParameterKey": "InstanceType", "ParameterValue": "t2.micro"}
]

# Create CloudFormation stack
print(f"Creating CloudFormation stack: {stack_name}")
response = cloudformation.create_stack(
    StackName=stack_name,
    TemplateBody=template_body,
    Parameters=parameters,
    Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],  # Required for IAM resources
)

# Get stack ID
stack_id = response["StackId"]
print(f"Stack creation initiated. Stack ID: {stack_id}")

# Wait for stack creation to complete
while True:
    stack_status = cloudformation.describe_stacks(StackName=stack_name)["Stacks"][0]["StackStatus"]
    print(f"Current stack status: {stack_status}")
    
    if stack_status in ["CREATE_COMPLETE", "CREATE_FAILED", "ROLLBACK_COMPLETE", "ROLLBACK_FAILED"]:
        break
    
    time.sleep(10)  # Wait before checking again

# Retrieve and print stack outputs if created successfully
if stack_status == "CREATE_COMPLETE":
    stack_info = cloudformation.describe_stacks(StackName=stack_name)["Stacks"][0]
    
    if "Outputs" in stack_info:
        print("\nStack Outputs:")
        for output in stack_info["Outputs"]:
            print(f"{output['OutputKey']}: {output['OutputValue']}")
    else:
        print("No outputs defined in the stack.")

elif stack_status in ["CREATE_FAILED", "ROLLBACK_COMPLETE", "ROLLBACK_FAILED"]:
    print("Stack creation failed. Check AWS CloudFormation console for details.")

print("Script execution complete.")
