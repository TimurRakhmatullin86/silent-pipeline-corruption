# Generator: deepseek-chat-v3-0324
# Task: af_046
# Generated: 2025-09-20T12:12:07Z

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

with DAG('af_046_pipeline', default_args=default_args, schedule='@daily', start_date=datetime(2025, 1, 1)) as dag:

    process_source = BigQueryInsertJobOperator(
        task_id='process_source',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.source`",
                "useLegacySql": False,
            }
        }
    )

    process_landing = BigQueryInsertJobOperator(
        task_id='process_landing',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.landing`",
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

    process_source >> process_landing
    process_landing >> process_target