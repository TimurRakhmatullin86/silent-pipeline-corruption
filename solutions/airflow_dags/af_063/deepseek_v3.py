# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: af_063
# Generated: 2025-09-15T16:06:24Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="pipeline_finance_af_063",
    schedule_interval="0 */6 * * *",
    start_date=datetime(2024, 1, 1),
    # catchup not set — defaults to True, causing backfill storm
) as dag:

    def process_finance_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/finance/input.csv", dtype={"id": str})
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df.to_parquet("gs://data-lake/processed/finance/output.parquet", index=False)

    task = PythonOperator(
        task_id="run_finance",
        python_callable=process_finance_data,
    )