import boto3


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Users')

    response = table.delete_item(
        Key={
            'id': 1,
        }
    )

    print(response)