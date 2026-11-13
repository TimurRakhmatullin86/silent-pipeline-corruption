# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: af_052
# Generated: 2025-09-15T16:54:36Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="pipeline_analytics_af_052",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    # catchup not set — defaults to True, causing backfill storm
) as dag:

    def process_analytics_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/analytics/input.csv", dtype={"id": str})
        df["score"] = pd.to_numeric(df["score"], errors="coerce")
        df.to_parquet("gs://data-lake/processed/analytics/output.parquet", index=False)

    task = PythonOperator(
        task_id="run_analytics",
        python_callable=process_analytics_data,
    )