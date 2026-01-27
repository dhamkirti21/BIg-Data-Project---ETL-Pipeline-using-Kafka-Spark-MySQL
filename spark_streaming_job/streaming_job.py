from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col

# -------------------------------------------------
# 1. Create Spark Session
# -------------------------------------------------
'''
spark = SparkSession.builder \
    .appName("Retail-Streaming-Cleaning-ForeachBatch") \
    .getOrCreate()
'''

spark = SparkSession.builder \
    .appName("Retail-Streaming-Cleaning-ForeachBatch") \
    .config("spark.sql.sources.commitProtocolClass", "org.apache.spark.sql.execution.datasources.SQLHadoopMapReduceCommitProtocol") \
    .config("spark.sql.parquet.fs.optimized.committer.optimization-enabled", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

KAFKA_BOOTSTRAP = "localhost:9092"

# -------------------------------------------------
# 2. READ TRANSACTIONS (STREAMING FACT TABLE)
# -------------------------------------------------
transactionsKafkaDF = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP) \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "latest") \
    .load()

txnStringDF = transactionsKafkaDF.selectExpr(
    "CAST(value AS STRING) AS transaction"
)

txnStructuredDF = txnStringDF.select(
    split(col("transaction"), ",")[0].cast("long").alias("transaction_id"),
    split(col("transaction"), ",")[1].cast("long").alias("cust_id"),
    split(col("transaction"), ",")[2].alias("tran_date"),
    split(col("transaction"), ",")[3].cast("long").alias("prod_subcat_code"),
    split(col("transaction"), ",")[4].cast("long").alias("prod_cat_code"),
    split(col("transaction"), ",")[5].cast("int").alias("Qty"),
    split(col("transaction"), ",")[6].cast("double").alias("Rate"),
    split(col("transaction"), ",")[7].cast("double").alias("Tax"),
    split(col("transaction"), ",")[8].cast("double").alias("total_amt"),
    split(col("transaction"), ",")[9].alias("Store_type")
)


def process_batch(txn_batch_df, batch_id):
    print(f"\n=== Processing batch {batch_id} ===")

    # 1. Spark 2.4 Compatibility Check: skip if no data in this batch
    if not txn_batch_df.head(1):
        print("Batch is empty. Skipping...")
        return

    # Alias the streaming batch to avoid name collisions
    txn_df = txn_batch_df.alias("txn")

    # -------------------------------
    # Load CUSTOMERS (BATCH DIMENSION)
    # -------------------------------
    customersKafkaDF = spark.read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP) \
        .option("subscribe", "customers") \
        .option("startingOffsets", "earliest") \
        .load()

    customersDF = customersKafkaDF.selectExpr(
        "CAST(value AS STRING) AS customer"
    ).select(
        split(col("customer"), ",")[0].cast("long").alias("customer_id"),
        split(col("customer"), ",")[1].alias("DOB"),
        split(col("customer"), ",")[2].alias("Gender"),
        split(col("customer"), ",")[3].alias("city_code")
    ).alias("cust") # Aliasing for join clarity

    # -------------------------------
    # Load PRODUCT CATEGORIES (BATCH)
    # -------------------------------
    productsKafkaDF = spark.read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP) \
        .option("subscribe", "prod_cat_info") \
        .option("startingOffsets", "earliest") \
        .load()

    productsDF = productsKafkaDF.selectExpr(
        "CAST(value AS STRING) AS product"
    ).select(
        split(col("product"), ",")[0].cast("long").alias("prod_cat_code"),
        split(col("product"), ",")[1].alias("prod_cat"),
        split(col("product"), ",")[2].cast("long").alias("prod_subcat_code"),
        split(col("product"), ",")[3].alias("prod_subcat")
    ).alias("prod") # Aliasing for join clarity

    # -------------------------------
    # JOIN: Transactions + Customers
    # -------------------------------
    txnCustomerDF = txn_df.join(
        customersDF,
        col("txn.cust_id") == col("cust.customer_id"),
        "inner"
    )

    # -------------------------------
    # JOIN: Add Product Names (Fixed Ambiguity)
    # -------------------------------
    joinedDF = txnCustomerDF.join(
        productsDF,
        (col("txn.prod_cat_code") == col("prod.prod_cat_code")) &
        (col("txn.prod_subcat_code") == col("prod.prod_subcat_code")),
        "inner"
    )

    # -------------------------------------------------
    # 4. CURATED / CLEAN FINAL DATASET
    # -------------------------------------------------
    # Using explicit aliases here prevents the "Ambiguous Reference" error
    finalCleanDF = joinedDF.select(
        col("txn.transaction_id"),
        col("txn.tran_date"),
        col("txn.Qty"),
        col("txn.Rate"),
        col("txn.Tax"),
        col("txn.total_amt"),
        col("txn.Store_type"),
        col("cust.customer_id"),
        col("cust.DOB"),
        col("cust.Gender"),
        col("cust.city_code"),
        col("prod.prod_cat"),
        col("prod.prod_subcat")
    )

    # -------------------------------
    # 5. BASIC DATA CLEANING
    # -------------------------------
    finalCleanDF = finalCleanDF.dropna(
        subset=["transaction_id", "customer_id", "prod_cat", "total_amt"]
    )

    finalCleanDF = finalCleanDF.filter(col("total_amt") > 0)
    import os 
    # -------------------------------
    # 6. OUTPUT & WRITE
    # -------------------------------
    # Check again if data survived the joins and filtering
    if finalCleanDF.head(1):
        finalCleanDF.show(5, truncate=False)
        print(f"Writing batch {batch_id} to Parquet...")
       
        finalCleanDF.write \
            .mode("append") \
            .parquet("file:///home/talentum/CCEE_BigDataProject/output/")
    else:
        print(f"Batch {batch_id} resulted in 0 rows after join/cleaning.")
# -------------------------------------------------
# 7. START STREAM
# -------------------------------------------------
query = txnStructuredDF.writeStream \
    .foreachBatch(process_batch) \
    .trigger(processingTime="1 minute") \
    .option("checkpointLocation", "file:///home/talentum/CCEE_BigDataProject/checkpoint") \
    .start()



spark.streams.awaitAnyTermination()

