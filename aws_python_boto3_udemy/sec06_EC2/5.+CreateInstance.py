import boto3



ec2_resource = boto3.resource('ec2')

response = ec2_resource.create_instances(
    ImageId='ami-033b95fb8079dc481',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='mykey',
    SecurityGroups=[
        'pygroup'
    ]
)

print(response)