# 🚀 Real-Time Retail Data ETL Pipeline using Kafka, Spark, MySQL & AWS S3
## 📌 Project Overview

This project demonstrates an end-to-end real-time data engineering pipeline built as an academic project to process retail transaction data using Apache Kafka, Apache Spark (Structured Streaming), MySQL, and AWS S3.

The pipeline ingests streaming retail data, performs real-time joins and transformations, stores curated data in Parquet format as a staging layer, and then loads the data into MySQL and AWS S3 for analytics and reporting.

The design focuses on fault tolerance, checkpointing, re-runnable execution, and separation of streaming and batch layers.

## 🏗️ Architecture Overview

```text
CSV Files
→ Kafka Producers
→ Kafka Topics
→ Spark Structured Streaming
→ Parquet (Local Data Lake)
→ Spark Batch Jobs
  ├── MySQL (Transactional Analytics)
  └── AWS S3 (Reporting / BI Storage)
```
![ChatGPT Image Feb 1, 2026, 10_30_34 PM](https://github.com/user-attachments/assets/55a8b140-7210-42e6-8e3f-48c5e5abd501)


## 🧰 Technology Stack
- Apache Kafka
- Apache Spark 2.4 (Structured Streaming)
- Apache Hadoop (Local File System)
- MySQL
- AWS S3
- Shell Scripting
- Python (PySpark)

## 📁 Project Structure

```text
CCEE_BigDataProject/
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
│ ├── parquet_to_mysql_job.py
│ └── parquet_to_s3_csv_job.py
│
├── scripts/
│ └── upload_to_s3.sh
│
├── output/ (Parquet data lake)
├── checkpoint/ (Spark checkpoints)
├── pipeline.sh
└── README.md
```
▶️ How to Run

Start the real-time pipeline:
```bash
bash pipeline.sh
```

🔁 Key Features
- Real-time ingestion using Kafka
- Structured Streaming with foreachBatch
- Fault-tolerant processing with checkpoints
- Parquet-based staging layer
- Re-runnable and idempotent pipeline
- Multiple downstream sinks (MySQL & S3)

## 📊 Use Cases
- Retail sales analytics
- Customer behavior analysis
- Product category performance
- BI reporting using cloud storage

## 🚀 Future Enhancements
- Apache Airflow orchestration (DAG-based scheduling)
- Tableau / Power BI integration using S3 data
- AWS Athena for serverless analytics
- Data quality validation framework
- Schema evolution handling

## 👤 Authors

Yuvaraj Kate — yuvarajkate1740@gmail.com

Dhamkirti Sisodia — dksisodia002@gmail.com
