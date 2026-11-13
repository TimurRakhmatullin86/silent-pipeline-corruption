# Generator: claude-sonnet-4-20250514
# Task: af_042
# Generated: 2025-08-05T10:26:56Z

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}

dag = DAG('af_042_pipeline', default_args=default_args, schedule_interval='@daily', start_date=datetime(2025, 1, 1))

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