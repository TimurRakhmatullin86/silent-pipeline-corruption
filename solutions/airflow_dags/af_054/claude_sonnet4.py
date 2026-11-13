# Generator: claude-sonnet-4-20250514
# Task: af_054
# Generated: 2025-09-21T19:28:57Z

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

dag = DAG('af_054_pipeline', default_args=default_args, schedule_interval='@daily', start_date=datetime(2025, 1, 1))

    process_source = BigQueryInsertJobOperator(
        task_id='process_source',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.source`",
                "useLegacySql": False,
            }
        }
    )

    process_staging_table = BigQueryInsertJobOperator(
        task_id='process_staging_table',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.staging_table`",
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

    process_source >> process_staging_table
    process_staging_table >> process_target