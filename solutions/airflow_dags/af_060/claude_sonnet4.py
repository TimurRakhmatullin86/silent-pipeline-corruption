# Generator: claude-sonnet-4-20250514
# Task: af_060
# Generated: 2025-09-13T09:29:04Z

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

dag = DAG('af_060_pipeline', default_args=default_args, schedule_interval='@daily', start_date=datetime(2025, 1, 1))

    process_source = BigQueryInsertJobOperator(
        task_id='process_source',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.source`",
                "useLegacySql": False,
            }
        }
    )

    process_stage = BigQueryInsertJobOperator(
        task_id='process_stage',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.stage`",
                "useLegacySql": False,
            }
        }
    )

    process_target = BigQueryInsertJobOperator(
        task_id='process_target',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.target`",
                "useLegacySql": False,
            }
        }
    )

    process_source >> process_stage
    process_stage >> process_target