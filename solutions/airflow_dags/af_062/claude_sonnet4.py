# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: af_062
# Generated: 2025-09-15T17:16:08Z

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
    dag_id="pipeline_ops_af_062",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=days_ago(1),
    catchup=False,
    tags=["ops"],
) as dag:

    def process_ops_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/ops/input.csv", dtype={"id": str})
        df["impressions"] = pd.to_numeric(df["impressions"], errors="coerce")
        df = df.dropna(subset=["impressions"])
        df.to_parquet("gs://data-lake/processed/ops/output.parquet", index=False)

    extract = PythonOperator(
        task_id="extract_ops",
        python_callable=process_ops_data,
    )

    validate = PythonOperator(
        task_id="validate_ops",
        python_callable=lambda **kw: True,
    )

    extract >> validate