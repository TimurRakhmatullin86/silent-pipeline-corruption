# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: af_072
# Generated: 2025-09-15T08:46:23Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="pipeline_logistics_af_072",
    schedule_interval="0 0 * * 1",
    start_date=datetime(2024, 1, 1),
    # catchup not set — defaults to True, causing backfill storm
) as dag:

    def process_logistics_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/logistics/input.csv", dtype={"id": str})
        df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
        df.to_parquet("gs://data-lake/processed/logistics/output.parquet", index=False)

    task = PythonOperator(
        task_id="run_logistics",
        python_callable=process_logistics_data,
    )