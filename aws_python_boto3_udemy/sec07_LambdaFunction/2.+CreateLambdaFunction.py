import boto3


iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')


with open('lambda.zip', 'rb') as f:
    zipped_code = f.read()


role = iam_client.get_role(RoleName='PyLambdaBasicExecution')

response = lambda_client.create_function(
    FunctionName='helloWorldLambda',
    Runtime='python3.9',
    Role=role['Role']['Arn'],
    Handler='lambda_function.lambda_handler',
    Code=dict(ZipFile=zipped_code),
    Timeout=300,

)

print(response)