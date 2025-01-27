## Write a Python script to create AWS APIGateway service of REST API with all available options and a lambda function with all available options to integrate with it 

import boto3
import json
import zipfile
import io
import time

# Initialize Boto3 clients for API Gateway, Lambda, and IAM
apigateway_client = boto3.client('apigateway')
lambda_client = boto3.client('lambda')
iam_client = boto3.client('iam')

#===========================================================================#
#################################### IAM ###################################
#===========================================================================#

# Create IAM role for Lambda function
role_name = 'LambdaExecutionRole'
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

# Wait a few seconds for the role to propagate
time.sleep(10)

#===========================================================================#
############################## Lambda Function ##############################
#===========================================================================#


# Create Lambda function
function_name = 'MyLambdaFunction'
runtime = 'python3.8'
handler = 'lambda_function.lambda_handler'

lambda_function_code = """
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
"""

# Create a zip file for the Lambda function code
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('lambda_function.py', lambda_function_code)
zip_buffer.seek(0)

lambda_response = lambda_client.create_function(
    FunctionName=function_name,
    Runtime=runtime,
    Role=role_arn,
    Handler=handler,
    Code={'ZipFile': zip_buffer.read()},
    Timeout=15,
    MemorySize=128
)
lambda_arn = lambda_response['FunctionArn']

#===========================================================================#
################################ API Gateway ################################
#===========================================================================#

# Create API Gateway REST API
api_name = 'MyRESTAPI'
api_response = apigateway_client.create_rest_api(
    name=api_name,
    description='My REST API',
    endpointConfiguration={
        'types': ['REGIONAL']
    },
    apiKeySource='HEADER'
)
api_id = api_response['id']

# Get the root resource ID
resources = apigateway_client.get_resources(restApiId=api_id)
root_id = [resource['id'] for resource in resources['items'] if resource['path'] == '/'][0]

# Create a resource
resource_response = apigateway_client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='myresource'
)
resource_id = resource_response['id']

# Create a method on the resource
method_response = apigateway_client.put_method(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

# Set up the Lambda integration
integration_response = apigateway_client.put_integration(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='GET',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f'arn:aws:apigateway:{lambda_client.meta.region_name}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
)

# Create deployment
deployment_response = apigateway_client.create_deployment(
    restApiId=api_id,
    stageName='dev'
)

# Add permission for API Gateway to invoke the Lambda function
lambda_client.add_permission(
    FunctionName=function_name,
    StatementId='APIGatewayInvoke',
    Action='lambda:InvokeFunction',
    Principal='apigateway.amazonaws.com',
    SourceArn=f'arn:aws:execute-api:{lambda_client.meta.region_name}:{boto3.client("sts").get_caller_identity()["Account"]}:{api_id}/*/GET/myresource'
)

# Print the API endpoint
api_endpoint = f'https://{api_id}.execute-api.{lambda_client.meta.region_name}.amazonaws.com/dev/myresource'
print(f'API Gateway endpoint: {api_endpoint}')
