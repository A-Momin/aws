#### Step 1: Create a crawler

#### Step 2: Start crawler and get crawler state in Step Function

#### Step 3: Inspect the Json of GetCrawler component to build the if-else condition

#### Step 4: Create a waiter block

#### Step 5: Add the Glue Run Job component (Below code)

-   Configure the block as synchronous component i.e. call the service, and have Step Functions wait for a job to complete

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

@params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "{}", table_name = "{}", transformation_ctx = "datasource0")

datasink4 = glueContext.write_dynamic_frame.from_options(frame = datasource0, connection_type = "s3",
connection_options = {"path": "s3://{}/{}/"}, format = "parquet", transformation_ctx = "datasink4")
job.commit()
```

#### Reusable Step Function Json:

```json
{
    "Comment": "A description of my state machine",
    "StartAt": "StartCrawler",
    "States": {
        "StartCrawler": {
            "Type": "Task",
            "Parameters": {
                "Name": "{Write the Crawler name here}"
            },
            "Resource": "arn:aws:states:::aws-sdk:glue:startCrawler",
            "Next": "GetCrawler"
        },
        "GetCrawler": {
            "Type": "Task",
            "Parameters": {
                "Name": "{Write the Crawler name here}"
            },
            "Resource": "arn:aws:states:::aws-sdk:glue:getCrawler",
            "Next": "Choice"
        },
        "Choice": {
            "Type": "Choice",
            "Choices": [
                {
                    "Variable": "$.Crawler.State",
                    "StringEquals": "RUNNING",
                    "Next": "Wait"
                }
            ],
            "Default": "Glue StartJobRun"
        },
        "Wait": {
            "Type": "Wait",
            "Seconds": 5,
            "Next": "GetCrawler"
        },
        "Glue StartJobRun": {
            "Type": "Task",
            "Resource": "arn:aws:states:::glue:startJobRun.sync",
            "Parameters": {
                "JobName": "{Write the Job name here}"
            },
            "End": true
        }
    }
}
```
