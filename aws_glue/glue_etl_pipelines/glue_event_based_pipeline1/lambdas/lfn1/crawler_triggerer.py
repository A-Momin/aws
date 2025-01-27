import json
import boto3

S3_CRAWLER_NAME = "httx-s3crawler"

glue=boto3.client('glue');

def lambda_handler(event, context):
    print(event)
    response = glue.start_crawler(
    Name=S3_CRAWLER_NAME
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
