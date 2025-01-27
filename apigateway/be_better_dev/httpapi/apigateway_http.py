## Write a Python script to create AWS APIGateway service of HTTP API with all available options and a lambda function with all available options to integrate with it 


import boto3
from botocore.exceptions import ClientError
import json
import zipfile
import io
import time


# Initialize Boto3 clients for Lambda and IAM
lambda_client = boto3.client('lambda')
iam_client = boto3.client('iam')
# Initialize Boto3 clients for API Gateway and Lambda
apigateway_v2_client = boto3.client('apigatewayv2')


#===========================================================================#
#################################### IAM ###################################
#===========================================================================#

def create_lambda_role(role_name):
    """
    Creates an IAM role for Lambda execution.

    Parameters:
    role_name (str): The name of the IAM role to create.

    Returns:
    str: The ARN of the created role.
    """
    assume_role_policy_document = json.dumps({
        'Version': '2012-10-17',
        'Statement': [{
            'Effect': 'Allow',
            'Principal': {'Service': 'lambda.amazonaws.com'},
            'Action': 'sts:AssumeRole'
        }]
    })

    role_response = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=assume_role_policy_document
    )
    role_arn = role_response['Role']['Arn']

    # Attach policy to the role
    policy_arn = 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )

    return role_arn


def delete_iam_role(role_name):
    """
    Deletes an AWS IAM role after detaching all associated policies and instance profiles.

    Parameters:
    role_name (str): The name of the IAM role to delete.
    
    Returns:
    dict: Response from the delete_role call.
    """
    try:
        # Detach all managed policies
        attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        for policy in attached_policies:
            iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])
        
        # Delete all inline policies
        inline_policies = iam_client.list_role_policies(RoleName=role_name)['PolicyNames']
        for policy_name in inline_policies:
            iam_client.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
        
        # Remove role from instance profiles
        instance_profiles = iam_client.list_instance_profiles_for_role(RoleName=role_name)['InstanceProfiles']
        for instance_profile in instance_profiles:
            iam_client.remove_role_from_instance_profile(InstanceProfileName=instance_profile['InstanceProfileName'], RoleName=role_name)

        # Delete the role
        response = iam_client.delete_role(RoleName=role_name)
        print(f"Role {role_name} has been deleted.")
        return response

    except ClientError as error:
        print(f"Error deleting role {role_name}: {error}")
        return None

# Example usage
# delete_iam_role('my_role_name')

#===========================================================================#
############################## Lambda Function ##############################
#===========================================================================#


def create_lambda_function(function_name, role_arn, zip_file_path, handler='apigateway_lambdahandler.lambda_handler'):
    """
    A Lambda function to be integrated with API Gateway.

    Parameters:
    function_name (str): The name of the Lambda function.
    role_arn (str): The ARN of the IAM role for Lambda execution.
    zip_file_path (str): The path to the zip file containing the Lambda function code.
    handler (str): The handler of the Lambda function.
    
    Returns:
    dict: Response from the create_function call.
    """

    with open(zip_file_path, 'rb') as f:
        zip_data = f.read()
    
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.8',
        Role=role_arn,
        Handler=handler,
        Code={'ZipFile': zip_data},
        Description='A Lambda function to be integrated with API Gateway',
        Timeout=15,
        MemorySize=128,
        Publish=True,
        # VpcConfig={
        #     'SubnetIds': [
        #         'subnet-xxxxxxxx',
        #     ],
        #     'SecurityGroupIds': [
        #         'sg-xxxxxxxx',
        #     ]
        # },
        Environment={
            'Variables': {
                'ENV_VAR_1': 'value1',
                'ENV_VAR_2': 'value2'
            }
        },
        TracingConfig={
            'Mode': 'Active'
        },
        Tags={
            'Project': 'LambdaDemo'
        }
    )
    
    return response

def update_lambda_function_zipfile(function_name, zip_file_path):
    """
    Updates the code of an existing Lambda function.

    Parameters:
    function_name (str): The name of the Lambda function.
    zip_file_path (str): The file path of the zip file containing the updated Lambda function code.
    
    Returns:
    dict: Response from the update_function_code call.
    """
    # Read the zip file into a bytes buffer
    with open(zip_file_path, 'rb') as zip_file:
        zip_buffer = zip_file.read()

    # Update the Lambda function code
    response = lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zip_buffer,
        Publish=True
    )
    
    return response

# Example usage
# response = update_lambda_function_code('my_lambda_function', 'path/to/updated_code.zip')
# print(response)


def delete_lambda_function(function_name):
    """
    Deletes a Lambda function.

    Parameters:
    function_name (str): The name of the Lambda function to delete.
    """
    lambda_client.delete_function(FunctionName=function_name)



#===========================================================================#
################################ API Gateway ################################
#===========================================================================#


def delete_http_api(api_id):
    """
    Deletes an API Gateway HTTP API.

    :param api_id: The ID of the HTTP API to delete.
    :return: Response from the delete_api call.
    """
    try:
        response = apigateway_v2_client.delete_api(
            ApiId=api_id
        )
        print(f"Deleted HTTP API with ID: {api_id}")
        return response
    except Exception as e:
        print(f"Error deleting HTTP API: {e}")



def create_all():

    # Create IAM role for Lambda function
    role_name = 'LambdaExecutionRoleDemo'
    role_arn = create_lambda_role(role_name)
    # print(role_arn) # Output: "arn:aws:iam::381492255899:role/LambdaExecutionRoleDemo"

    # Wait a few seconds for the role to propagate
    time.sleep(10)



    # # # Create Lambda function example
    function_name = "apigateway_lambda_function"
    zip_file_path = "lambdahandler.zip"
    # role_arn = "arn:aws:iam::381492255899:role/LambdaExecutionRoleDemo"

    response = create_lambda_function(function_name, role_arn, zip_file_path)
    # print(response)



    # Create API Gateway HTTP API
    api_name = 'MyHTTPAPI'
    api_response = apigateway_v2_client.create_api(
        Name=api_name,
        ProtocolType='HTTP',
        RouteKey='GET /',
        Target=f'arn:aws:apigateway:{lambda_client.meta.region_name}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
    )
    api_id = api_response['ApiId']

    # Create Lambda permission for API Gateway
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId='APIGatewayAccess',
        Action='lambda:InvokeFunction',
        Principal='apigateway.amazonaws.com',
        SourceArn=f'arn:aws:execute-api:{lambda_client.meta.region_name}:{boto3.client("sts").get_caller_identity()["Account"]}:{api_id}/*/*'
    )

    # Print the API endpoint
    api_endpoint = f'https://{api_id}.execute-api.{lambda_client.meta.region_name}.amazonaws.com'
    print(f'API Gateway endpoint: {api_endpoint}')

# def delete_all():
#     delete_iam_role(role_name)
#     delete_lambda_function(function_name)
