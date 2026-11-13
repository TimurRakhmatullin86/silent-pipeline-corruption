# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: af_041
# Generated: 2025-09-15T17:28:44Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="pipeline_ops_af_041",
    schedule_interval="0 0 * * 1",
    start_date=datetime(2024, 1, 1),
    # catchup not set — defaults to True, causing backfill storm
) as dag:

    def process_ops_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/ops/input.csv", dtype={"id": str})
        df["clicks"] = pd.to_numeric(df["clicks"], errors="coerce")
        df.to_parquet("gs://data-lake/processed/ops/output.parquet", index=False)

    task = PythonOperator(
        task_id="run_ops",
        python_callable=process_ops_data,
    )