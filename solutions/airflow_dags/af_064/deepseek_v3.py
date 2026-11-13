# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: af_064
# Generated: 2025-09-15T19:51:54Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="pipeline_marketing_af_064",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    # catchup not set — defaults to True, causing backfill storm
) as dag:

    def process_marketing_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/marketing/input.csv", dtype={"id": str})
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
        df.to_parquet("gs://data-lake/processed/marketing/output.parquet", index=False)

    task = PythonOperator(
        task_id="run_marketing",
        python_callable=process_marketing_data,
    )