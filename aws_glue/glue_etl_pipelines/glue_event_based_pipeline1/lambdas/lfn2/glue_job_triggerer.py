import json
import boto3

JOB_NAME = 'jb1_s3csv_s3parquet'


def lambda_handler(event, context):
    glue=boto3.client('glue');
    response = glue.start_job_run(JobName = JOB_NAME)
    print("Lambda Invoke")
 