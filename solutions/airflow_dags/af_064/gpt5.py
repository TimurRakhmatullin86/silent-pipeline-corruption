# Generator: gpt-5-2025-08-07
# Task: af_064
# Generated: 2025-09-27T12:21:19Z

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

with DAG(
    dag_id='af_064_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    tags=['data-pipeline', 'airflow_dag'],
) as dag:

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

    process_dead_letter_table = BigQueryInsertJobOperator(
        task_id='process_dead_letter_table',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.dead_letter_table`",
                "useLegacySql": False,
            }
        }
    )

    process_source >> process_staging_table
    process_staging_table >> process_dead_letter_table