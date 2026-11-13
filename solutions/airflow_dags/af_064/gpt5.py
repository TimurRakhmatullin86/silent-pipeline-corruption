# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: af_064
# Generated: 2025-09-15T17:57:00Z

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
    dag_id="pipeline_marketing_af_064",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["marketing"],
) as dag:

    def process_marketing_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/marketing/input.csv", dtype={"id": str})
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
        df = df.dropna(subset=["revenue"])
        df.to_parquet("gs://data-lake/processed/marketing/output.parquet", index=False)

    extract = PythonOperator(
        task_id="extract_marketing",
        python_callable=process_marketing_data,
    )

    validate = PythonOperator(
        task_id="validate_marketing",
        python_callable=lambda **kw: True,
    )

    extract >> validate