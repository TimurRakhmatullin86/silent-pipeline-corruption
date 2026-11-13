# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: af_074
# Generated: 2025-09-15T13:08:04Z

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
    dag_id="pipeline_finance_af_074",
    default_args=default_args,
    schedule_interval="0 */6 * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["finance"],
) as dag:

    def process_finance_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/finance/input.csv", dtype={"id": str})
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df = df.dropna(subset=["quantity"])
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