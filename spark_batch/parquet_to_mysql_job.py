#!/usr/bin/env python3

from pyspark.sql import SparkSession

# -------------------------------------------------
# 1. Spark Session
# -------------------------------------------------
spark = SparkSession.builder \
    .appName("ParquetToMySQLJob") \
    .master("local[*]") \
    .getOrCreate()

# -------------------------------------------------
# 2. Paths & JDBC Config
# -------------------------------------------------
PARQUET_PATH = "file:///home/talentum/CCEE_BigDataProject/output"

MYSQL_URL = "jdbc:mysql://127.0.0.1:3306/projectdb?useSSL=false&allowPublicKeyRetrieval=true"
MYSQL_TABLE = "retail_transactions"

MYSQL_PROPERTIES = {
    "user": "bigdata",
    "password": "Bigdata@123",
    "driver": "com.mysql.jdbc.Driver"
}

# -------------------------------------------------
# 3. Read Parquet
# -------------------------------------------------
df = spark.read.parquet(PARQUET_PATH)

print("Parquet schema:")
df.printSchema()

print("Sample data:")
df.show(5, truncate=False)

# -------------------------------------------------
# 4. Write to MySQL
# -------------------------------------------------
df.write \
    .mode("overwrite") \
    .jdbc(
        url=MYSQL_URL,
        table=MYSQL_TABLE,
        properties=MYSQL_PROPERTIES
    )

print("Data successfully written to MySQL")

spark.stop()

