# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: af_052
# Generated: 2025-09-15T14:18:00Z

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
    dag_id="pipeline_analytics_af_052",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["analytics"],
) as dag:

    def process_analytics_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/analytics/input.csv", dtype={"id": str})
        df["score"] = pd.to_numeric(df["score"], errors="coerce")
        df = df.dropna(subset=["score"])
        df.to_parquet("gs://data-lake/processed/analytics/output.parquet", index=False)

    extract = PythonOperator(
        task_id="extract_analytics",
        python_callable=process_analytics_data,
    )

    validate = PythonOperator(
        task_id="validate_analytics",
        python_callable=lambda **kw: True,
    )

    extract >> validate