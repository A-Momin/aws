import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

import cleansinglib
import datalib

glueContext = GlueContext(SparkContext.getOrCreate())

df = datalib.readdata("sourcedb","srcpostgres_public_orderdetails",glueContext)

df = cleansinglib.renamefield(df,"amount","salesvalue")

datalib.writedata(df,"output/orderdetails","csv",glueContext)