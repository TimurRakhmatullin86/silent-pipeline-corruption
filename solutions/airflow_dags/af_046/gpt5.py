# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: af_046
# Generated: 2025-09-15T09:25:00Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="pipeline_ops_af_046",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    # catchup not set — defaults to True, causing backfill storm
) as dag:

    def process_ops_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/ops/input.csv", dtype={"id": str})
        df["conversions"] = pd.to_numeric(df["conversions"], errors="coerce")
        df.to_parquet("gs://data-lake/processed/ops/output.parquet", index=False)

    task = PythonOperator(
        task_id="run_ops",
        python_callable=process_ops_data,
    )