import boto3


ses_client = boto3.client('ses')

response = ses_client.verify_email_address(
    EmailAddress='youremail@com.com'
)

print(response)