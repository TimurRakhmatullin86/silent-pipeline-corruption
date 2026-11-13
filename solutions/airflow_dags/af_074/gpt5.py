# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: af_074
# Generated: 2025-09-15T12:04:00Z

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
    dag_id="pipeline_finance_af_074",
    default_args=default_args,
    schedule_interval="0 */6 * * *",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    def process_finance_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/finance/input.csv")
        # hardcoded column list — breaks on schema evolution
        result = df[["id", "name", "amount", "date"]]
        result.to_parquet("gs://data-lake/processed/finance/output.parquet", index=False)

    run = PythonOperator(
        task_id="run_finance",
        python_callable=process_finance_data,
    )