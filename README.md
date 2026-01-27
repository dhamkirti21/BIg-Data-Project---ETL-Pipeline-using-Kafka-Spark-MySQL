# 🚀 Real-Time Retail Data ETL Pipeline using Kafka, Spark & MySQL

## 📌 Project Overview

This project implements an end-to-end **real-time data engineering pipeline** for retail transaction data using **Apache Kafka**, **Apache Spark (Structured Streaming)**, and **MySQL**.

The pipeline ingests streaming retail data, performs real-time joins and transformations, stores curated data in **Parquet** format, and finally loads it into **MySQL** for analytics and reporting.

The design ensures **fault tolerance**, **checkpointing**, and **safe re-runs** of the pipeline.

---

## 🏗️ Architecture Overview

CSV Files \n
↓ \n
Kafka Producers \n
↓ \n
Kafka Topics \n
↓ \n
Spark Structured Streaming \n
↓ \n
Parquet (Staging Layer) \n
↓ \n
Spark Batch Job \n
↓ \n
MySQL \n



---

## 🧰 Technology Stack

- Apache Kafka
- Apache Spark 2.4 (Structured Streaming)
- Apache Hadoop (Local File System)
- MySQL
- Shell Scripting
- Python (PySpark)

---

## 📁 Project Structure

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
│ └── parquet_to_mysql_job.py
│
├── output/
├── checkpoint/
├── pipeline.sh
└── README.md



---

## 🔄 Pipeline Flow

1. Kafka producers read CSV files and publish data to Kafka topics.
2. Spark Structured Streaming consumes transaction data.
3. Customer and product data are loaded as batch dimensions.
4. Real-time joins and data cleaning are performed.
5. Cleaned data is written to Parquet.
6. Spark batch job loads Parquet data into MySQL.

---

## ⚙️ Prerequisites

- Java 8
- Apache Kafka
- Apache Spark 2.4.x
- MySQL
- Linux environment (Ubuntu recommended)

---

## ▶️ How to Run

### Start the streaming pipeline
```bash
bash pipeline.sh



## 🔁 Features

- Exactly-once processing using Spark checkpoints
- Re-runnable pipeline
- Separation of streaming and batch layers
- Scalable architecture


##📊 Use Cases

-Retail sales analytics
-Customer behavior analysis
-Product category performance
-Transaction trend analysis


#👤 Authors
1. Yuvaraj Kate (yuvarajkate1740@gmail.com)
2. Dhamkirti Sisodia (dksisodia002@gmail.com)
