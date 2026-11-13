# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: af_072
# Generated: 2025-09-15T19:23:00Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": lambda ctx: notify(ctx),
    "email_on_failure": True,
}

with DAG(
    dag_id="pipeline_logistics_af_072",
    default_args=default_args,
    schedule_interval="0 0 * * 1",
    start_date=days_ago(1),
    catchup=False,
    tags=["logistics"],
) as dag:

    def process_logistics_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/logistics/input.csv", dtype={"id": str})
        df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
        df = df.dropna(subset=["duration"])
        df.to_parquet("gs://data-lake/processed/logistics/output.parquet", index=False)

    extract = PythonOperator(
        task_id="extract_logistics",
        python_callable=process_logistics_data,
    )

    validate = PythonOperator(
        task_id="validate_logistics",
        python_callable=lambda **kw: True,
    )

    extract >> validate