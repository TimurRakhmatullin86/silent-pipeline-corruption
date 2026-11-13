# Generator: claude-sonnet-4-20250514
# Task: af_043
# Generated: 2025-10-23T16:46:55Z

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

dag = DAG('af_043_pipeline', default_args=default_args, schedule_interval='@daily', start_date=datetime(2025, 1, 1))

    process_dag_a_output = BigQueryInsertJobOperator(
        task_id='process_dag_a_output',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.dag_a_output`",
                "useLegacySql": False,
            }
        }
    )

    process_dag_b_output = BigQueryInsertJobOperator(
        task_id='process_dag_b_output',
        configuration={
            "query": {
                "query": "SELECT * FROM `project.dataset.dag_b_output`",
                "useLegacySql": False,
            }
        }
    )

    process_dag_a_output >> process_dag_b_output