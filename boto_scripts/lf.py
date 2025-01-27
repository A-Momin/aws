import boto3
import botocore
from botocore.exceptions import ClientError

# =============================================================================
glue_client = boto3.client('glue')
lakeformation_client = boto3.client('lakeformation')
sts_client = boto3.client('sts')
# =============================================================================

def create_glue_database(database_name, catalog_id=None, description=None, location_uri=None, parameters=None, use_only_iam_access_control=False):
    """
    Create a database in AWS Glue.

    :param catalog_id: The ID of the Data Catalog in which to create the database.
    :param database_name: The name of the database.
    :param description: (Optional) A description of the database.
    :param location_uri: (Optional) The location of the database.
    :param parameters: (Optional) A dictionary of key-value pairs that define parameters and properties of the database.
    :param use_only_iam_access_control: (Optional) Whether to use only IAM access control for new tables in this database.
    :return: Response from the AWS Glue create_database call.
    """

    # Create the database input dictionary
    database_input = {'Name': database_name}

    if description: database_input['Description'] = description

    if location_uri: database_input['LocationUri'] = location_uri

    if parameters: database_input['Parameters'] = parameters

    # Call the create_database function
    response = glue_client.create_database(
        CatalogId=catalog_id,
        DatabaseInput=database_input
    )

    # Set the UseOnlyIamAccessControl property using Lake Formation API
    if use_only_iam_access_control:
        lakeformation_client.update_database(
            CatalogId=catalog_id,
            Name=database_name,
            DatabaseInput={
                'Name': database_name,
                'UseOnlyIamAccessControl': use_only_iam_access_control
            }
        )

    return response

# register the Amazon S3 bucket as your data lake storage
def register_s3_path_as_data_lake_location(s3_path, iam_role='AWSServiceRoleForLakeFormationDataAccess'):
    """
    Register an S3 path as the storage location for your data lake with AWS Lake Formation.

    :param s3_path: The S3 URI of the path (e.g., s3://example-bucket/path/).
    :param iam_role: The IAM role to use for access (default is 'AWSServiceRoleForLakeFormationDataAccess').
    :return: None
    """

    # Convert the S3 path to the bucket ARN
    bucket_name = s3_path.split("//")[1].split("/")[0]
    s3_bucket_arn = f'arn:aws:s3:::{bucket_name}'

    # Get the account ID of the IAM role
    account_id = sts_client.get_caller_identity().get('Account')

    # Construct the ARN for the IAM role
    role_arn = f'arn:aws:iam::{account_id}:role/{iam_role}'

    try:
        response = lakeformation_client.register_resource(
            ResourceArn=s3_bucket_arn,
            UseServiceLinkedRole=True,  # Set to False to use the provided IAM role instead of the service-linked role
            RoleArn=role_arn,
            HybridAccessEnabled=True
        )
        print(f"Location registered successfully: {response}")
    except ClientError as e:
        print(f"Error registering location: {e}")

def grant_permissions(role_user_group_arn, resources, permissions=['ALL'], grantable_permissions=['ALL']):
    """
    Grant database permissions to a role in AWS Lake Formation.

    :param database_name: The name of the database to which permissions are granted.
    :param role_arn: The ARN of the IAM role to which permissions are granted.
    :param permissions: List of permissions to grant (e.g., ['ALL', 'SELECT', 'DESCRIBE']).
    :return: None
    """

    try:
        response = lakeformation_client.grant_permissions(
            CatalogId=None,
            Principal={
                'DataLakePrincipalIdentifier': role_user_group_arn
            },
            Resource=resources,
            Permissions=permissions,
            PermissionsWithGrantOption=grantable_permissions
        )

        print(f"Permissions granted successfully: {response}")
    except ClientError as e:
        print(f"Error granting permissions: {e}")

def grant_database_level_permissions(database_name, role_user_group_arn, permissions):
    """
    Grant database permissions to a role in AWS Lake Formation.

    :param database_name: The name of the database to which permissions are granted.
    :param role_user_group_arn: The ARN of the IAM role to which permissions are granted.
    :param permissions: List of permissions to grant (e.g., ['ALL', 'SELECT', 'DESCRIBE']).
    :return: None
    """

    try:
        response = lakeformation_client.grant_permissions(
            Principal={
                'DataLakePrincipalIdentifier': role_user_group_arn
            },
            Resource={
                'Database': {
                    'Name': database_name
                }
            },
            Permissions=permissions,
            PermissionsWithGrantOption=permissions  # If you want to allow the role to grant these permissions to others
        )
        print(f"Permissions granted successfully: {response}")
    except ClientError as e:
        print(f"Error granting permissions: {e}")

def grant_table_level_permissions(principal, database_name, table_name, permissions=['ALL'], grant_option=False):
    """
    Grant table permissions to an IAM role in AWS Lake Formation.
    
    :param principal: The ARN of the IAM role or user.
    :param database_name: The name of the database in Lake Formation.
    :param table_name: The name of the table in the database.
    :param permissions: A list of permissions to grant (e.g., ['SELECT', 'ALTER']).
    :param grant_option: Boolean to grant permissions with grant option (default is False).
    """

    try:
        # Define the permissions with or without grant option
        permissions_with_grant_option = permissions if grant_option else []
        
        # Grant permissions on the table
        response = lakeformation_client.grant_permissions(
            Principal={
                'DataLakePrincipalIdentifier': principal
            },
            Resource={
                'Table': {
                    'DatabaseName': database_name,
                    'Name': table_name
                }
            },
            Permissions=permissions,
            PermissionsWithGrantOption=permissions_with_grant_option
        )
        
        print(f"Permissions granted successfully to {principal} for table {table_name} in database {database_name}")
        return response

    except Exception as e:
        print(f"Error granting permissions: {e}")


# response = glue_client.delete_table(
#             DatabaseName=database_name,
#             Name=table_name
#         )



if __name__ == "__main__":
    resources={
        'Catalog': {}
        ,
        'Database': {
            'CatalogId': 'string',
            'Name': 'string'
        },
        'Table': {
            'CatalogId': 'string',
            'DatabaseName': 'string',
            'Name': 'string',
            'TableWildcard': {}

        },
        'TableWithColumns': {
            'CatalogId': 'string',
            'DatabaseName': 'string',
            'Name': 'string',
            'ColumnNames': [
                'string',
            ],
            'ColumnWildcard': {
                'ExcludedColumnNames': [
                    'string',
                ]
            }
        },
        'DataLocation': {
            'CatalogId': 'string',
            'ResourceArn': 'string'
        },
        'DataCellsFilter': {
            'TableCatalogId': 'string',
            'DatabaseName': 'string',
            'TableName': 'string',
            'Name': 'string'
        },
        'LFTag': {
            'CatalogId': 'string',
            'TagKey': 'string',
            'TagValues': [
                'string',
            ]
        },
        'LFTagPolicy': {
            'CatalogId': 'string',
            'ResourceType': 'DATABASE'|'TABLE',
            'Expression': [
                {
                    'TagKey': 'string',
                    'TagValues': [
                        'string',
                    ]
                },
            ]
        }
    },

    permissions=['ALL'], # Other Options: 'SELECT', 'ALTER', 'DROP', 'DELETE', 'INSERT', 'DESCRIBE', 'CREATE_DATABASE', 'CREATE_TABLE', 'DATA_LOCATION_ACCESS', 'CREATE_LF_TAG', 'ASSOCIATE', 'GRANT_WITH_LF_TAG_EXPRESSION'
    grantable_permissions=['ALL'] # Other Options: 'SELECT', 'ALTER', 'DROP', 'DELETE', 'INSERT', 'DESCRIBE', 'CREATE_DATABASE', 'CREATE_TABLE', 'DATA_LOCATION_ACCESS', 'CREATE_LF_TAG', 'ASSOCIATE', 'GRANT_WITH_LF_TAG_EXPRESSION'

    grant_permissions(resources, permissions, grantable_permissions)