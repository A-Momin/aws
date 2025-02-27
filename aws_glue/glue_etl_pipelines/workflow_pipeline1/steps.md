-   [Knowledge Amplifier: AWS Glue Workflow in-depth intuition with Lab](https://www.youtube.com/watch?v=KC9t2yEyVSE&t=90s)

## Step 1:

Create a s3 bucket with 2 folders

## Step 2:

Create a Glue role

## Step 3:

Create a Glue Database

## Step 4:

Create 2 Glue Crawlers

## Step 5:

Create a Glue job with Job bookmark enabled--

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "workflowdemoyt", table_name = "csvstorer", transformation_ctx = "datasource0")

datasink4 = glueContext.write_dynamic_frame.from_options(frame = datasource0, connection_type = "s3",
connection_options = {"path": "s3://{}/{}/"}, format = "parquet", transformation_ctx = "datasink4")
job.commit()
```

## Step 6:

Create the Glue Workflow

## Step 7:

Download the Snowflake data --
`sql select * from books where publishyear=2002 and PUBLISHMONTH=23;`

## Step 8:

Trigger the Glue workflow

## Step 9:

Query using Athena--

## Step 10:

Download the Snowflake data --
`sql select * from books where publishyear=2001 and PUBLISHMONTH=1;`

## Step 11:

Trigger the Glue workflow

## Step 12:

Query using Athena--
