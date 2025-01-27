import boto3
from pprint import pprint


ses_client = boto3.client('ses')

'''
response = ses_client.get_template(
    TemplateName='CustomTemplate'
)

pprint(response['Template'])
'''

response = ses_client.list_templates()
print(response['TemplatesMetadata'])