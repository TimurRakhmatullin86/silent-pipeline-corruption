# Generator: gpt-5-2025-08-07
# Task: af_051
# Generated: 2025-10-28T12:29:54Z

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
    dag_id='af_051_pipeline',
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

    process_audit_table = BigQueryInsertJobOperator(
        task_id='process_audit_table',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.audit_table`",
                "useLegacySql": False,
            }
        }
    )

    process_source >> process_target
    process_target >> process_audit_table