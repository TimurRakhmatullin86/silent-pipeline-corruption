# Generator: gpt-5-2025-08-07
# Task: af_067
# Generated: 2025-08-21T11:51:38Z

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
    dag_id='af_067_pipeline',
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

    process_target = BigQueryInsertJobOperator(
        task_id='process_target',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.target`",
                "useLegacySql": False,
            }
        }
    )

    process_source >> process_target