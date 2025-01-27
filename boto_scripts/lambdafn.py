import boto3
import os, json, zipfile, io, time, shutil, subprocess
from io import BytesIO
from pathlib import Path


ACCOUNT_ID = os.environ['AWS_ACCOUNT_ID_ROOT']
REGION = os.environ['AWS_DEFAULT_REGION']
VPC_ID = 'vpc-03617a8a518caa526'
DEFAULT_SUBNET_IDS = ['subnet-0980ad10eb313405b', 'subnet-0de97821ddb8236f7', 'subnet-0a160fbe0fcafe373', 'subnet-0ca765b361e4cb186', 'subnet-0a972b05a5b162feb']
SUBNET_ID = DEFAULT_SUBNET_IDS[0]
DEFAULT_SECURITY_GROUP_ID = 'sg-07f4ccd7a5be677ea'


# Initialize Boto3 clients for Lambda and IAM
lambda_client = boto3.client('lambda')
iam_client = boto3.client('iam')

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

def create_lambda_function(function_name, role_arn, zip_file_path, handler):
    """
    Creates a Lambda function with all possible options.

    Parameters:
    function_name (str): The name of the Lambda function.
    role_arn (str): The ARN of the IAM role for Lambda execution.
    zip_file_path (str): The path to the zip file containing the Lambda function code.
    handler (str): The handler of the Lambda function.
    
    Returns:
    dict: Response from the create_function call.
    """
    lambda_client = boto3.client('lambda')
    
    with open(zip_file_path, 'rb') as f:
        zip_data = f.read()
    
    response = lambda_client.create_function(
        FunctionName=function_name,
        Description='A sample Lambda function with all possible options',
        Runtime='python3.8',
        Role=role_arn,
        Handler=handler,
        Code={'ZipFile': zip_data},
        Timeout=60,         # Timeout in seconds
        MemorySize=128,     # Memory size in MB
        Publish=True,       # Set to True to publish a new version
        # Environment={
        #     'Variables': {
        #         'ENV_VAR_1': 'value1',
        #         'ENV_VAR_2': 'value2'
        #     }
        # },
        # VpcConfig={
        #     'SubnetIds': DEFAULT_SUBNET_IDS,
        #     'SecurityGroupIds': [DEFAULT_SECURITY_GROUP_ID,]
        # },
        # TracingConfig={
        #     'Mode': 'Active'
        # },
        # Tags={
        #     'Project': 'LambdaDemo'
        # },
        # Layers=[
        #     'arn:aws:lambda:us-east-1:123456789012:layer:my-layer:1',
        # ],
        # DeadLetterConfig={
        #     'TargetArn': 'arn:aws:sqs:us-east-1:123456789012:my-queue'
        # },
        # KMSKeyArn='arn:aws:kms:us-east-1:123456789012:key/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
        # FileSystemConfigs=[
        #     {
        #         'Arn': 'arn:aws:efs:us-east-1:123456789012:access-point/fsap-xxxxxxxxxxxxxxxxx',
        #         'LocalMountPath': '/mnt/efs'
        #     },
        # ],
    )
    
    return response

def update_lambda_function_code(function_name, zip_buffer):
    """
    Updates the code of an existing Lambda function.

    Parameters:
    function_name (str): The name of the Lambda function.
    zip_buffer (BytesIO): The zip file containing the updated Lambda function code.
    
    Returns:
    dict: Response from the update_function_code call.
    """
    return lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zip_buffer.read(),
        Publish=True
    )

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

def delete_lambda_function(function_name):
    """
    Deletes a Lambda function.

    Parameters:
    function_name (str): The name of the Lambda function to delete.
    """
    lambda_client.delete_function(FunctionName=function_name)

def zip_lambda_function_to_zip_file(source_dir, output_filename, requirements_file=None):
    """
    Zips a Python module as an AWS Lambda handler.

    :param source_dir: The directory containing the lambda function code.
    :param output_filename: The name of the output zip file.
    :param requirements_file: Path to the requirements.txt file (optional).
    """
    # Create a temporary directory to assemble the lambda package
    temp_dir = Path("temp_lambda_package")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    # Copy the source files to the temporary directory
    for item in os.listdir(source_dir):
        source_path = Path(source_dir) / item
        destination_path = temp_dir / item
        if source_path.is_dir():
            shutil.copytree(source_path, destination_path)
        else:
            shutil.copy2(source_path, destination_path)

    # Install the dependencies if requirements.txt is provided
    if requirements_file:
        subprocess.check_call([
            "pip", "install", "-r", requirements_file, 
            "-t", str(temp_dir)
        ])

    # Create the zip file
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                zipf.write(file_path, file_path.relative_to(temp_dir))

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

    print(f"Lambda function packaged as {output_filename}")

def zip_lambda_function_to_zip_buffer(source_dir, requirements_file=None):
    """
    Zips a Python module as an AWS Lambda handler.

    :param source_dir: The directory containing the lambda function code.
    :param requirements_file: Path to the requirements.txt file (optional).
    :return: BytesIO object containing the zipped lambda function.
    """
    # Create a temporary directory to assemble the lambda package
    temp_dir = Path("temp_lambda_package")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    # Copy the source files to the temporary directory
    for item in os.listdir(source_dir):
        source_path = Path(source_dir) / item
        destination_path = temp_dir / item
        if source_path.is_dir():
            shutil.copytree(source_path, destination_path)
        else:
            shutil.copy2(source_path, destination_path)

    # Install the dependencies if requirements_file is provided
    if requirements_file:
        subprocess.check_call([
            "pip", "install", "-r", requirements_file, 
            "-t", str(temp_dir)
        ])

    # Create the zip file in-memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                zipf.write(file_path, file_path.relative_to(temp_dir))

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

    zip_buffer.seek(0)  # Rewind the buffer to the beginning
    return zip_buffer

def create_lambda_package(lfn_scripts=[], package_dir=".", **kwargs):
    """
    Creates a deployable AWS Lambda package by bundling Python scripts, dependencies, and optional directories into a ZIP file.

    Args:
        lfn_scripts (list, optional): 
            A list of Python script file paths to include in the Lambda package. Only `.py` files are included. 
            Defaults to an empty list.
        package_dir (str, optional): 
            The directory where the resulting `package.zip` will be saved. Defaults to the current directory.
        **kwargs: 
            Additional optional keyword arguments:
            - requirements_file (str): Path to a `requirements.txt` file specifying Python dependencies to install in the package.
            - py_libs (list): A list of Python libraries to install using `pip`. These libraries are added directly to the package.
            - lfn_repo (str): Path to a directory containing additional files or resources to include in the package.

    Raises:
        subprocess.CalledProcessError: 
            If a subprocess command (e.g., virtual environment creation, dependency installation) fails.
        FileNotFoundError: 
            If a Python script in `lfn_scripts`, the `requirements_file`, or the `lfn_repo` does not exist.
        PermissionError: 
            If file or directory permissions prevent copying, writing, or deletion.

    Example:
        >>> create_lambda_package(
                lfn_scripts=["handler.py", "helper.py"],
                package_dir="./output",
                requirements_file="requirements.txt",
                py_libs=["boto3", "requests"],
                lfn_repo="./lambda_resources"
            )
        Package created successfully at ./output/package.zip

    Side Effects:
        - Creates a temporary directory to hold intermediate files.
        - Creates a virtual environment in the temporary directory to manage dependencies.
        - Produces a `package.zip` file in the specified `package_dir`.
        - Cleans up the temporary directory after packaging is complete.

    Returns:
        None
    """

    # Create temporary directory
    temp_dir = Path.cwd() / 'temp_dir'
    temp_dir.mkdir(exist_ok=True)

    # Create virtual environment
    venv_dir = temp_dir / 'venv'
    subprocess.run(['python3', '-m', 'venv', venv_dir])

    # Activate the virtual environment
    if os.name == 'nt':  # Windows
        activate_script = venv_dir / 'Scripts' / 'activate'
    else:  # Unix/Linux/MacOS
        activate_script = venv_dir / 'bin' / 'activate'

    activate_command = f"source {activate_script}"

    # Install dependencies from requirements.txt if provided
    requirements_file = kwargs.get('requirements_file', "")
    if requirements_file:
        subprocess.run(f"{activate_command} && pip install -r {requirements_file}", shell=True, check=True)

    lfn_repo = kwargs.get('lfn_repo', "")
    if lfn_repo:
        # Copy contents of lfn_repo to temp_dir
        for item in Path(lfn_repo).iterdir():
            target = temp_dir / item.name
            if item.is_dir(): shutil.copytree(item, target)
            else: shutil.copy2(item, target)

    if lfn_scripts:
        for item in lfn_scripts:
            if os.path.isfile(item) and item.endswith('.py'):
                # Construct the target path
                target_path = os.path.join(temp_dir, os.path.basename(item))
                shutil.copy(item, target_path)

    # Install dependencies from the py_libs list if provided
    py_libs = kwargs.get('py_libs', [])
    if py_libs:
        subprocess.run(f"""{activate_command} && pip install {" ".join(py_libs)} -t {temp_dir}""", shell=True, check=True)


    # Create package.zip and save it to package_dir
    package_zip = Path(package_dir) / 'package.zip'
    with zipfile.ZipFile(package_zip, 'w') as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                full_path = Path(root) / file
                arcname = full_path.relative_to(temp_dir)
                zipf.write(full_path, arcname)

    # Clean up by removing the virtual environment and temp_dir
    shutil.rmtree(temp_dir)

    print(f"Package created successfully at {package_zip}")


def zipfile_to_zipcode(zipfile_path):
    # Create Lambda function
    with open(zipfile_path, 'rb') as f:
        zipped_code = f.read()
    return zipped_code


def create_lambda_layer(layer_name, description, zip_file_path, runtime, compatible_runtimes):
    """
    Creates an AWS Lambda layer.

    Args:
        layer_name (str): The name of the Lambda layer.
        description (str): A description of the Lambda layer.
        zip_file_path (str or Path): The path to the .zip file containing the layer contents.
        runtime (str): The runtime environment for the layer (e.g., 'python3.8').
        compatible_runtimes (list): List of compatible runtimes (e.g., ['python3.8', 'python3.9']).

    Returns:
        dict: The response from the `create_layer_version` API call.
    """

    # Initialize the boto3 client for Lambda
    lambda_client = boto3.client('lambda')

    # Read the .zip file as binary
    with open(zip_file_path, 'rb') as zip_file:
        layer_zip_content = zip_file.read()

    # Create the Lambda layer
    response = lambda_client.create_layer_version(
        LayerName=layer_name,
        Description=description,
        Content={'ZipFile': layer_zip_content},
        CompatibleRuntimes=compatible_runtimes
    )

    return response


def attach_layer_to_lambda(function_name, layer_arn):
    """
    Attaches a layer to an existing AWS Lambda function.

    Args:
        function_name (str): The name or ARN of the Lambda function.
        layer_arn (str): The ARN of the layer to attach.

    Returns:
        dict: The response from the `update_function_configuration` API call.
    """

    # Initialize the boto3 client for Lambda
    lambda_client = boto3.client('lambda')

    # Get the existing configuration to retrieve current layers
    current_config = lambda_client.get_function_configuration(FunctionName=function_name)
    existing_layers = current_config.get('Layers', [])

    # Extract ARNs of existing layers, if any
    existing_layer_arns = [layer['Arn'] for layer in existing_layers]

    # Add the new layer ARN to the list
    new_layers = existing_layer_arns + [layer_arn]

    # Update the function configuration to include the new layer
    response = lambda_client.update_function_configuration(
        FunctionName=function_name,
        Layers=new_layers
    )

    return response

def print_latest_lambda_logs(function_name):
    # Initialize the CloudWatch Logs client
    logs_client = boto3.client('logs', region_name=REGION)  # Replace with your region
    
    # Log group name for the Lambda function
    log_group_name = f"/aws/lambda/{function_name}"
    
    try:
        # Get the log streams for the log group
        response = logs_client.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=1  # Only fetch the latest log stream
        )
        
        log_streams = response.get('logStreams', [])
        if not log_streams:
            print(f"No log streams found for Lambda function: {function_name}")
            return

        # print(log_streams)
        # Get the latest log stream name
        latest_log_stream = log_streams[0]['logStreamName']
        print(f"Latest log stream: {latest_log_stream}")
        
        # Fetch log events from the latest log stream
        log_events_response = logs_client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=latest_log_stream,
            startFromHead=True  # Set to True to get events from the start
        )
        
        print("Log Events:")
        for event in log_events_response.get('events', []):
            print(event['message'])
    
    except Exception as e:
        print(f"Error fetching logs for Lambda function {function_name}: {e}")



# ####=======================

# ### Adding S3 as a trigger for a Lambda function

# # Create a Lambda and S3 client
# lambda_client = boto3.client('lambda')
# s3_client = boto3.client('s3')

# # Define the Lambda function ARN and S3 bucket name
# lambda_function_arn = 'arn:aws:lambda:region:account-id:function:function-name'
# bucket_name = 'your-bucket-name'

# # Add S3 trigger to the Lambda function
# response = s3_client.put_bucket_notification_configuration(
#     Bucket=bucket_name,
#     NotificationConfiguration={
#         'LambdaFunctionConfigurations': [
#             {
#                 'LambdaFunctionArn': lambda_function_arn,
#                 'Events': [
#                     's3:ObjectCreated:*'  # Trigger Lambda on object creation
#                 ]
#             }
#         ]
#     }
# )

# print(response)
# # ------------------------

# ### Adding DynamoDB Stream as a trigger for a Lambda function

# # Create clients for Lambda and DynamoDB
# lambda_client = boto3.client('lambda')
# dynamodb_client = boto3.client('dynamodb')

# # Define the Lambda function ARN and DynamoDB table name
# lambda_function_arn = 'arn:aws:lambda:region:account-id:function:function-name'
# table_name = 'your-table-name'

# # Get the stream ARN from the DynamoDB table
# response = dynamodb_client.describe_table(TableName=table_name)
# stream_arn = response['Table']['LatestStreamArn']

# # Add DynamoDB stream as a trigger to the Lambda function
# lambda_client.create_event_source_mapping(
#     EventSourceArn=stream_arn,
#     FunctionName=lambda_function_arn,
#     StartingPosition='LATEST'
# )

# print("DynamoDB Stream trigger added to Lambda")


# ### ==========================

# ### Adding SNS Topic as a trigger for a Lambda function

# import boto3

# # Create a Lambda and SNS client
# lambda_client = boto3.client('lambda')
# sns_client = boto3.client('sns')

# # Define the Lambda function ARN and SNS topic ARN
# lambda_function_arn = 'arn:aws:lambda:region:account-id:function:function-name'
# sns_topic_arn = 'arn:aws:sns:region:account-id:topic-name'

# # Subscribe the Lambda function to the SNS topic
# response = sns_client.subscribe(
#     TopicArn=sns_topic_arn,
#     Protocol='lambda',
#     Endpoint=lambda_function_arn
# )

# # Give the Lambda function permission to be triggered by SNS
# lambda_client.add_permission(
#     FunctionName=lambda_function_arn,
#     StatementId='sns-lambda-trigger',
#     Action='lambda:InvokeFunction',
#     Principal='sns.amazonaws.com',
#     SourceArn=sns_topic_arn
# )

# print("SNS trigger added to Lambda")


# ### ============================

# # Create a Lambda and SNS client
# lambda_client = boto3.client('lambda')
# sns_client = boto3.client('sns')

# # Define the Lambda function ARN and SNS topic ARN
# lambda_function_arn = 'arn:aws:lambda:region:account-id:function:function-name'
# sns_topic_arn = 'arn:aws:sns:region:account-id:topic-name'

# # Subscribe the Lambda function to the SNS topic
# response = sns_client.subscribe(
#     TopicArn=sns_topic_arn,
#     Protocol='lambda',
#     Endpoint=lambda_function_arn
# )

# Give the Lambda function permission to be triggered by SNS
response = # Grant EventBridge permission to invoke the Lambda function
lambda_client.add_permission(
    FunctionName='LFN_JOB_TRIGGERER_NAME',
    StatementId=f"{'S3_RAW_CRAWLER_RULE_NAME'}-invoke-permission",
    Action="lambda:InvokeFunction",
    Principal="events.amazonaws.com",
    SourceArn='S3_RAW_CRAWLER_RULE_ARN'
)

# print("SNS trigger added to Lambda")
