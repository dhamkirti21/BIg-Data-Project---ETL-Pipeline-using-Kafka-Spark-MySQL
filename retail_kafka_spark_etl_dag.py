from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

PROJECT_HOME = "/home/talentum/CCEE_BigDataProject"
KAFKA_HOME = "/home/talentum/kafka"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
}

dag = DAG(
    dag_id="retail_kafka_spark_etl",
    default_args=default_args,
    description="Real-Time Retail Data ETL using Kafka, Spark & MySQL",
    schedule_interval=None,   # manual trigger
    start_date=days_ago(1),
    catchup=False,
)

cleanup = BashOperator(
    task_id="cleanup_previous_run",
    bash_command=f"""
    rm -rf {PROJECT_HOME}/checkpoint
    rm -rf {PROJECT_HOME}/output
    """,
    dag=dag,
)

start_zookeeper = BashOperator(
    task_id="start_zookeeper",
    bash_command=f"""
    nohup {KAFKA_HOME}/bin/zookeeper-server-start.sh \
    {KAFKA_HOME}/config/zookeeper.properties > /tmp/zookeeper.log 2>&1 &
    sleep 10
    """,
    dag=dag,
)

start_kafka = BashOperator(
    task_id="start_kafka",
    bash_command=f"""
    nohup {KAFKA_HOME}/bin/kafka-server-start.sh \
    {KAFKA_HOME}/config/server.properties > /tmp/kafka.log 2>&1 &
    sleep 15
    """,
    dag=dag,
)

produce_customers = BashOperator(
    task_id="produce_customers",
    bash_command=f"bash -c {PROJECT_HOME}/kafka_scripts/customer.sh",
    dag=dag,
)

produce_products = BashOperator(
    task_id="produce_products",
    bash_command=f"bash -c {PROJECT_HOME}/kafka_scripts/prod_cat_info.sh",
    dag=dag,
)

produce_transactions = BashOperator(
    task_id="produce_transactions",
    bash_command=f"bash -c {PROJECT_HOME}/kafka_scripts/transactions.sh",
    dag=dag,
)

spark_streaming = BashOperator(
    task_id="spark_streaming_job",
    bash_command=f"""
    spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 \
    {PROJECT_HOME}/spark_streaming_job/streaming_job.py
    """,
    dag=dag,
)

spark_batch_mysql = BashOperator(
    task_id="spark_batch_to_mysql",
    bash_command=f"""
    spark-submit \
    {PROJECT_HOME}/spark_batch/parquet_to_mysql_job.py
    """,
    dag=dag,
)

cleanup >> start_zookeeper >> start_kafka
start_kafka >> produce_customers >> produce_products >> produce_transactions
produce_transactions >> spark_streaming >> spark_batch_mysql

