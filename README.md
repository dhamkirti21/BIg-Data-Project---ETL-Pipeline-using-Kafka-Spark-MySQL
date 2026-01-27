# 🚀 Real-Time Retail Data ETL Pipeline using Kafka, Spark & AWS S3

## 📌 Project Overview

This project implements an end-to-end **real-time data engineering pipeline** for retail transaction data using **Apache Kafka**, **Apache Spark (Structured Streaming)**, and **Amazon S3**.

The pipeline ingests streaming retail data, performs real-time joins and transformations, stores curated data in **Parquet** format as a staging layer, and finally converts it into **CSV files stored in AWS S3** for downstream analytics and visualization.

The design ensures **fault tolerance**, **checkpointing**, and **safe re-runs** of the pipeline.

---

## 🏗️ Architecture Overview

CSV Files
➡ Kafka Producers
➡ Kafka Topics
➡ Spark Structured Streaming
➡ Parquet (Staging Layer – Local Filesystem)
➡ Spark Batch Job
➡ AWS S3 (CSV Data Lake)

---

## 🧰 Technology Stack

* Apache Kafka
* Apache Spark 2.4 (Structured Streaming & Batch)
* Apache Hadoop (Local File System)
* AWS S3
* Apache Airflow
* Shell Scripting
* Python (PySpark)

---

## 📁 Project Structure

```text
CCEE_BigDataProject/
│
├── Dataset/
│ ├── Customer.csv
│ ├── prod_cat_info.csv
│ └── Transactions.csv
│
├── kafka_scripts/
│ ├── customer.sh
│ ├── prod_cat_info.sh
│ └── transactions.sh
│
├── spark_streaming_job/
│ └── streaming_job.py
│
├── spark_batch/
│ ├── parquet_validation_job.py
│ └── parquet_to_s3_csv_job.py
│
├── airflow_dags/
│ └── retail_kafka_spark_etl_dag.py
|
├── scripts/
│ └── upload_to_S3.sh
│
├── output/        # Parquet staging layer
├── checkpoint/    # Spark streaming checkpoints
├── pipeline.sh
└── README.md
```

---

## 🔄 Pipeline Flow

1. Kafka producers read CSV files and publish data to Kafka topics.
2. Spark Structured Streaming consumes transaction data from Kafka.
3. Customer and product data are loaded as batch reference datasets.
4. Real-time joins, filtering, and data cleaning are performed.
5. Cleaned data is written to **Parquet files** on the local filesystem.
6. Spark batch job reads Parquet files and uploads **CSV outputs to AWS S3**.

---

## ⚙️ Prerequisites

* Java 8
* Apache Kafka
* Apache Spark 2.4.x
* Apache Airflow
* AWS Account (Free Tier)
* AWS CLI configured
* Linux environment (Ubuntu recommended)

---

## ▶️ How to Run

### Run using Shell Script

```bash
bash pipeline.sh
```

### Run using Airflow

```bash
airflow webserver
airflow scheduler
```

Trigger the DAG:
**`retail_kafka_spark_etl`**

---

## 🛠️ Airflow DAG Details

The pipeline is orchestrated using **Apache Airflow** with the following tasks:

* Cleanup previous output and checkpoint directories
* Start ZooKeeper
* Start Kafka Broker
* Produce customer data to Kafka
* Produce product category data to Kafka
* Produce transaction data to Kafka
* Run Spark Structured Streaming job
* Run Spark batch job to upload CSV files to AWS S3

The DAG is designed to be **idempotent** and can be safely re-run multiple times.

---

## 🔁 Features

* Fault-tolerant streaming using Spark checkpoints
* Re-runnable and idempotent pipeline
* Separation of streaming and batch processing layers
* Cloud-ready data lake using AWS S3
* Orchestration using Apache Airflow
* Scalable and modular design

---

## 📊 Tableau / BI Integration (Planned)

* CSV data stored in AWS S3 will be used as a data source
* Data can be connected to:

  * Tableau (via extracted CSV or Athena)
  * Power BI
  * Other BI and analytics tools
* Enables interactive dashboards for:

  * Sales trends
  * Customer insights
  * Product performance

---

## 🚀 Future Enhancements

* Add AWS Glue / Athena for serverless querying
* Enable incremental S3 partitioning by date
* Implement schema evolution handling
* Add data quality checks using Great Expectations
* Deploy on Docker / Kubernetes
* Integrate real-time dashboards
* Add alerting and monitoring

---

## 📊 Use Cases

* Retail sales analytics
* Customer behavior analysis
* Product category performance
* Transaction trend analysis
* Data lake creation for BI tools

---

## 👤 Authors

1. **Yuvaraj Kate** — [yuvarajkate1740@gmail.com](mailto:yuvarajkate1740@gmail.com)
2. **Dhamkirti Sisodia** — [dksisodia002@gmail.com](mailto:dksisodia002@gmail.com)

---

Just say the word 👌
