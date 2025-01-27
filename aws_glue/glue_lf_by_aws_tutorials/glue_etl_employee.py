import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

bucket_name = 'httx-datalake-bkt'
catalog_db_name = 'httx-catalog-db'
src_catalog_table_name = 'interview_questions_employee'
des_catalog_table_name = 'transformed_employee'

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Relational DB
employee_relational_db_node = glueContext.create_dynamic_frame.from_catalog(
    database=catalog_db_name,
    table_name=src_catalog_table_name,
    transformation_ctx="employee_relational_db_node",
)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.getSink(
    path=f"s3://{bucket_name}/employees/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="S3bucket_node3",
)

S3bucket_node3.setCatalogInfo(
    catalogDatabase=catalog_db_name, catalogTableName=des_catalog_table_name
)
S3bucket_node3.setFormat("glueparquet")
S3bucket_node3.writeFrame(employee_relational_db_node)
job.commit()
