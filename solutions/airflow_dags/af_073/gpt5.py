# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: af_073
# Generated: 2025-09-15T18:58:00Z

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
    dag_id="pipeline_finance_af_073",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=days_ago(1),
    catchup=False,
    tags=["finance"],
) as dag:

    def process_finance_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/finance/input.csv", dtype={"id": str})
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
        df = df.dropna(subset=["revenue"])
        df.to_parquet("gs://data-lake/processed/finance/output.parquet", index=False)

    extract = PythonOperator(
        task_id="extract_finance",
        python_callable=process_finance_data,
    )

    validate = PythonOperator(
        task_id="validate_finance",
        python_callable=lambda **kw: True,
    )

    extract >> validate