#!/bin/bash

source ~/unset_jupyter.sh

PROJECT_HOME=$(pwd)
KAFKA_HOME=$HOME/kafka

echo "Starting ZooKeeper..."
gnome-terminal --title="ZooKeeper" -- bash -c "
$KAFKA_HOME/bin/zookeeper-server-start.sh \
$KAFKA_HOME/config/zookeeper.properties;
exec bash
"

sleep 10

echo "Starting Kafka Broker..."
gnome-terminal --title="Kafka Broker" -- bash -c "
$KAFKA_HOME/bin/kafka-server-start.sh \
$KAFKA_HOME/config/server.properties;
exec bash
"

sleep 15

echo "Pushing customers..."
gnome-terminal --title="Customers Producer" -- bash -c "
$PROJECT_HOME/kafka_scripts/customer.sh;
exec bash
"

sleep 5

echo "Pushing products..."
gnome-terminal --title="Products Producer" -- bash -c "
$PROJECT_HOME/kafka_scripts/prod_cat_info.sh;
exec bash
"

sleep 5

echo "Pushing transactions..."
gnome-terminal --title="Transactions Producer" -- bash -c "
$PROJECT_HOME/kafka_scripts/transactions.sh;
exec bash
"

sleep 10

echo "Starting Spark Streaming Job..."
gnome-terminal --title="Spark Streaming" -- bash -c "
spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 \
$PROJECT_HOME/spark_streaming_job/streaming_job.py;
exec bash
"

# -------------------------------------------------
# WAIT for streaming to write parquet
# -------------------------------------------------
echo "Waiting for parquet files to be generated..."
sleep 90

# -------------------------------------------------
# PARQUET → MYSQL (Batch Job)
# -------------------------------------------------
echo "Loading parquet data into MySQL..."
spark-submit \
--jars $HOME/spark/jars/mysql-connector-java-5.1.49.jar \
$PROJECT_HOME/spark_batch/parquet_to_mysql_job.py


# ------------------------------
# Upload to S3
# ------------------------------
echo "Uploading data to S3..."
$PROJECT_HOME/scripts/upload_to_s3.sh

echo "PIPELINE EXECUTION COMPLETED"

echo "Pipeline completed successfully."

