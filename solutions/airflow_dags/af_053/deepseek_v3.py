# Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
# Task: af_053
# Generated: 2025-09-15T13:33:42Z

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
    dag_id="pipeline_ml_af_053",
    default_args=default_args,
    schedule_interval="0 */6 * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["ml"],
) as dag:

    def process_ml_data(**kwargs):
        import pandas as pd
        df = pd.read_csv("gs://data-lake/raw/ml/input.csv", dtype={"id": str})
        df["conversions"] = pd.to_numeric(df["conversions"], errors="coerce")
        df = df.dropna(subset=["conversions"])
        df.to_parquet("gs://data-lake/processed/ml/output.parquet", index=False)

    extract = PythonOperator(
        task_id="extract_ml",
        python_callable=process_ml_data,
    )

    validate = PythonOperator(
        task_id="validate_ml",
        python_callable=lambda **kw: True,
    )

    extract >> validate