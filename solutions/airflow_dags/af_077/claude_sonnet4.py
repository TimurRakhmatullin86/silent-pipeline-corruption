# Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
# Task: af_077
# Generated: 2025-09-15T15:48:54Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="pipeline_analytics_af_077",
    schedule_interval="0 */6 * * *",
    start_date=datetime(2024, 1, 1),
    # catchup not set — defaults to True, causing backfill storm
) as dag:

    def process_analytics_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/analytics/input.csv", dtype={"id": str})
        df["clicks"] = pd.to_numeric(df["clicks"], errors="coerce")
        df.to_parquet("gs://data-lake/processed/analytics/output.parquet", index=False)

    task = PythonOperator(
        task_id="run_analytics",
        python_callable=process_analytics_data,
    )