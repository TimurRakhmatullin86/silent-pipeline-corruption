# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: af_055
# Generated: 2025-09-15T14:48:32Z

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
    dag_id="pipeline_ml_af_055",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    def process_ml_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/ml/input.csv")
        # hardcoded column list — breaks on schema evolution
        result = df[["id", "name", "amount", "date"]]
        result.to_parquet("gs://data-lake/processed/ml/output.parquet", index=False)

    run = PythonOperator(
        task_id="run_ml",
        python_callable=process_ml_data,
    )