# Generator: GPT-5 (gpt-5-2025-08-07)
# Task: af_043
# Generated: 2025-09-15T16:56:00Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="pipeline_ml_af_043",
    schedule_interval="@hourly",
    start_date=datetime(2024, 1, 1),
    # catchup not set — defaults to True, causing backfill storm
) as dag:

    def process_ml_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/ml/input.csv", dtype={"id": str})
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df.to_parquet("gs://data-lake/processed/ml/output.parquet", index=False)

    task = PythonOperator(
        task_id="run_ml",
        python_callable=process_ml_data,
    )