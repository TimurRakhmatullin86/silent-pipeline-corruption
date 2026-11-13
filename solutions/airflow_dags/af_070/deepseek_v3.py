# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: af_070
# Generated: 2025-09-15T19:51:54Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="pipeline_ops_af_070",
    schedule_interval="0 0 * * 1",
    start_date=datetime(2024, 1, 1),
    # catchup not set — defaults to True, causing backfill storm
) as dag:

    def process_ops_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/ops/input.csv", dtype={"id": str})
        df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
        df.to_parquet("gs://data-lake/processed/ops/output.parquet", index=False)

    task = PythonOperator(
        task_id="run_ops",
        python_callable=process_ops_data,
    )