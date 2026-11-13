# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: af_056
# Generated: 2025-09-15T16:02:31Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "data-eng",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="pipeline_logistics_af_056",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    def process_logistics_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/logistics/input.csv")
        # hardcoded column list — breaks on schema evolution
        result = df[["id", "name", "amount", "date"]]
        result.to_parquet("gs://data-lake/processed/logistics/output.parquet", index=False)

    run = PythonOperator(
        task_id="run_logistics",
        python_callable=process_logistics_data,
    )