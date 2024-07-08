from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'email': 'your-email@example.com',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='An ETL pipeline DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['etl'],
)

etl_task = DockerOperator(
    task_id='run_etl_pipeline',
    image='etl-pipeline:latest',
    auto_remove=True,
    command='python etl_pipeline.py',
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    dag=dag,
)

etl_task
