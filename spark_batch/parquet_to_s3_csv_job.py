#!/usr/bin/env python3

from pyspark.sql import SparkSession
from pyspark.sql.functions import year, month, dayofmonth, to_date

spark = SparkSession.builder \
    .appName("ParquetToS3CSV") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "com.amazonaws.auth.DefaultAWSCredentialsProviderChain"
    ) \
    .getOrCreate()

# Local parquet produced by streaming job
INPUT_PATH = "file:///home/talentum/CCEE_BigDataProject/output"

# S3 target (CHANGE BUCKET NAME)
S3_PATH = "s3a://ccee-bigdata-project/retail/transactions/csv"

# Read parquet
df = spark.read.parquet(INPUT_PATH)

# Convert date safely (important)
df = df.withColumn(
    "tran_date_parsed",
    to_date("tran_date", "d/M/yyyy")
)

# Add partitions
df = df.withColumn("year", year("tran_date_parsed")) \
       .withColumn("month", month("tran_date_parsed")) \
       .withColumn("day", dayofmonth("tran_date_parsed"))

# Write to S3 as CSV
df.write \
  .mode("append") \
  .option("header", "true") \
  .partitionBy("year", "month", "day") \
  .csv(S3_PATH)

spark.stop()

