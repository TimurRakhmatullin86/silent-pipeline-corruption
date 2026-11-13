# Generator: deepseek-chat-v3-0324
# Task: af_042
# Generated: 2025-10-31T13:24:38Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'catchup': True,
}

with DAG('af_042_pipeline', default_args=default_args, schedule='@daily', start_date=datetime(2025, 1, 1)) as dag:

    process_source_path = BigQueryInsertJobOperator(
        task_id='process_source_path',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.source_path`",
                "useLegacySql": False,
            }
        }
    )

    process_target_table = BigQueryInsertJobOperator(
        task_id='process_target_table',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.target_table`",
                "useLegacySql": False,
            }
        }
    )

    process_source_path >> process_target_table