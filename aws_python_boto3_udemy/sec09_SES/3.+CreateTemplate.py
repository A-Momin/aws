import boto3

ses_client = boto3.client('ses')

response = ses_client.create_template(
    Template={
        'TemplateName':'CustomTemplate',
        'SubjectPart':'Welcome to the course',
        'TextPart':'Thanks for buying the course',
        'HtmlPart':'Thanks for buying the course'
    }
)

print(response)