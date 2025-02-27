-   [Intro to Amazon EMR - Big Data Tutorial using Spark](https://www.youtube.com/watch?v=8bOgOvz6Tcg&t=667s)

<details><summary style="font-size:20px;color:Red">How to Test it Locally?</summary>

-   **Assumptions**:

    -   Following Environment Variable are Configured:
        -   `export PYSPARK_PYTHON="python3"`
        -   `export PYSPARK_DRIVER_PYTHON="python3"`
        -   `export SPARK_HOME="/usr/local/spark-3.3.3-bin-hadoop3"`
        -   `export PATH=$SPARK_HOME/bin:$PATH`
        -   `export PATH="/usr/local/opt/openjdk@11/bin:${PATH}"`

-   `$ cae ds-env` --> Activate Conada environment which contain PySpark
-   `$ spark-submit emr_tutorial/main.py --data_source $DATA/restaurant_violations.csv --output_uri $DATA/TEST` --> Submit your PySpark to the Cluster.

</details>

-   **Instance Profile**:

    -   An instance profile is a container for an IAM role that you can attach to an EC2 instance.
    -   It grants the EC2 instance the permissions defined in the associated IAM role.

-   **Cluster Describtion**:

```json
{
    'Cluster': {
        'Id': 'j-2TJQ9EB28UDB4',
        'Name': 'http-emr-cluster-2024-12-05',
        'Status': {
            'State': 'WAITING',
            'StateChangeReason': {'Message': 'Cluster ready to run steps.'},
            'Timeline': {
                'CreationDateTime': datetime.datetime(2024, 12, 5, 13, 6, 43, 650000, tzinfo=tzlocal()),
                'ReadyDateTime': datetime.datetime(2024, 12, 5, 13, 12, 3, 125000, tzinfo=tzlocal())
            }
        },
        'Ec2InstanceAttributes': {
            'Ec2KeyName': 'AMominNJ',
            'Ec2SubnetId': 'subnet-0980ad10eb313405b',
            'RequestedEc2SubnetIds': ['subnet-0980ad10eb313405b'],
            'Ec2AvailabilityZone': 'us-east-1f',
            'RequestedEc2AvailabilityZones': [],
            'IamInstanceProfile': 'AmazonEMR-InstanceProfile-20241205T130626',
            'EmrManagedMasterSecurityGroup': 'sg-05199d215981f1520',
            'EmrManagedSlaveSecurityGroup': 'sg-013cd214cf27146c6',
            'AdditionalMasterSecurityGroups': [],
            'AdditionalSlaveSecurityGroups': []
        },
        'InstanceCollectionType': 'INSTANCE_GROUP',
        'LogUri': "s3n://emr-2024-12-05/monthly-build/2024-12-05/logs/",
        'ReleaseLabel': 'emr-6.12.0',
        'AutoTerminate': False,
        'TerminationProtected': False,
        'UnhealthyNodeReplacement': False,
        'VisibleToAllUsers': True,
        'Applications': [{'Name': 'Spark', 'Version': '3.4.0'}, {'Name': 'Zeppelin', 'Version': '0.10.1'}],
        'Tags': [{'Key': 'for-use-with-amazon-emr-managed-policies', 'Value': 'true'}],
        'ServiceRole': 'arn:aws:iam::381492255899:role/service-role/AmazonEMR-ServiceRole-20241205T130642',
        'NormalizedInstanceHours': 0,
        'MasterPublicDnsName': 'ec2-44-210-19-244.compute-1.amazonaws.com',
        'Configurations': [],
        'ScaleDownBehavior': 'TERMINATE_AT_TASK_COMPLETION',
        'KerberosAttributes': {},
        'ClusterArn': 'arn:aws:elasticmapreduce:us-east-1:381492255899:cluster/j-2TJQ9EB28UDB4',
        'StepConcurrencyLevel': 1,
        'PlacementGroups': [],
        'OSReleaseLabel': '2.0.20241031.0'
    },
    'ResponseMetadata': {
        'RequestId': '87ae20aa-a09a-4f07-88ed-781bf2dd389d',
        'HTTPStatusCode': 200,
        'HTTPHeaders': {
            'x-amzn-requestid': '87ae20aa-a09a-4f07-88ed-781bf2dd389d',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '1598',
            'date': 'Thu, 05 Dec 2024 19:47:27 GMT'
        },
        'RetryAttempts': 0
    }
}
```
