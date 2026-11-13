# Generator: deepseek-chat-v3-0324
# Task: af_050
# Generated: 2025-10-27T13:42:22Z

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

with DAG('af_050_pipeline', default_args=default_args, schedule='@daily', start_date=datetime(2025, 1, 1)) as dag:

    process_source = BigQueryInsertJobOperator(
        task_id='process_source',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.source`",
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

    process_variable = BigQueryInsertJobOperator(
        task_id='process_variable',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.variable`",
                "useLegacySql": False,
            }
        }
    )

    process_source >> process_target
    process_target >> process_variable