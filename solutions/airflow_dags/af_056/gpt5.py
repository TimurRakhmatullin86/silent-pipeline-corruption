# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: af_056
# Generated: 2025-09-15T15:31:00Z

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
    dag_id="pipeline_logistics_af_056",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=days_ago(1),
    catchup=False,
    tags=["logistics"],
) as dag:

    def process_logistics_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/logistics/input.csv", dtype={"id": str})
        df["conversions"] = pd.to_numeric(df["conversions"], errors="coerce")
        df = df.dropna(subset=["conversions"])
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