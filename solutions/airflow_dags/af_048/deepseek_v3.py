# Generator: deepseek-chat-v3-0324
# Task: af_048
# Generated: 2025-09-27T16:14:39Z

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

with DAG('af_048_pipeline', default_args=default_args, schedule='@daily', start_date=datetime(2025, 1, 1)) as dag:

    process_source = BigQueryInsertJobOperator(
        task_id='process_source',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.source`",
                "useLegacySql": False,
            }
        }
    )

    process_watermark_table = BigQueryInsertJobOperator(
        task_id='process_watermark_table',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.watermark_table`",
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

    process_source >> process_watermark_table
    process_watermark_table >> process_target