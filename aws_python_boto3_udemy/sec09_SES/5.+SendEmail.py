import boto3

ses_client = boto3.client('ses')

resp = ses_client.send_templated_email(
    Source='admin@geekscoders.com',
    Destination={
        'ToAddresses':['youremail@com.com','youremail2@com.com'],
        'CcAddresses':['youremail@com.com']
    },
    ReplyToAddresses=['youremail@com.com'],
    Template='CustomTemplate',
    TemplateData='{"replace":"value"}'
)

print(resp)