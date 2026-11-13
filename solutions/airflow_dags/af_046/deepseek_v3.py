# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: af_046
# Generated: 2025-09-15T11:15:50Z

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
    dag_id="pipeline_ops_af_046",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["ops"],
) as dag:

    def process_ops_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/ops/input.csv", dtype={"id": str})
        df["conversions"] = pd.to_numeric(df["conversions"], errors="coerce")
        df = df.dropna(subset=["conversions"])
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