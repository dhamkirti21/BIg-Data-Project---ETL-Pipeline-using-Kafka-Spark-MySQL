#!/usr/bin/env python3

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ParquetValidationJob") \
    .master("local[*]") \
    .getOrCreate()

PARQUET_PATH = "file:///home/talentum/CCEE_BigDataProject/output"

df = spark.read.parquet(PARQUET_PATH)

df.printSchema()
df.show(10, truncate=False)

print("Total rows:", df.count())


spark.stop()

