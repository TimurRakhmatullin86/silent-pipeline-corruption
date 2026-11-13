# Generator: claude-sonnet-4-20250514
# Task: af_049
# Generated: 2025-09-13T16:22:43Z

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

dag = DAG('af_049_pipeline', default_args=default_args, schedule_interval='@daily', start_date=datetime(2025, 1, 1))

    process_source = BigQueryInsertJobOperator(
        task_id='process_source',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.source`",
                "useLegacySql": False,
            }
        }
    )

    process_rates_table = BigQueryInsertJobOperator(
        task_id='process_rates_table',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.rates_table`",
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

    process_source >> process_rates_table
    process_rates_table >> process_target