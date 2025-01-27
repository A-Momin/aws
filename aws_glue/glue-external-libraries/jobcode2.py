import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

import cleansinglib
import datalib

glueContext = GlueContext(SparkContext.getOrCreate())

df = datalib.readdata("sourcedb","srcpostgres_public_customers",glueContext)

datalib.writedata(df,"output/customers","json",glueContext)