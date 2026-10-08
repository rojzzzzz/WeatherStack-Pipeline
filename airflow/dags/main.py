from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.standard.operators.python import PythonOperator
from docker.types import Mount
import pendulum
import sys
import os

sys.path.append('/opt/airflow/api-request')


def upload_weather_data():
    from insert_records import uploader

    uploader()


with DAG(
    dag_id='weather_data_pipeline',
    description='Extracts weather data and loads it into PostgreSQL',
    start_date=pendulum.datetime(2026, 10, 7, tz='UTC'),
    schedule='@daily',
    catchup=False,
    max_active_runs=1,
) as dag:
    upload_task = PythonOperator(
        task_id='uploader',
        python_callable=upload_weather_data,
        retries=3,
        retry_delay=pendulum.duration(minutes=5),
        execution_timeout=pendulum.duration(hours=1),
    )

    transform_task = DockerOperator(
        task_id='transform_data',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='build',
        working_dir='/usr/app',
        mounts=[
            Mount(
                source=os.environ['DBT_PROJECT_HOST_PATH'],
                target='/usr/app',
                type='bind',
            ),
            Mount(
                source=os.environ['DBT_PROFILES_HOST_PATH'],
                target='/root/.dbt',
                type='bind',
            ),
        ],
        environment={
            'DBT_PROFILES_DIR': '/root/.dbt',
            'POSTGRES_ROOT_PASSWORD': os.environ['POSTGRES_ROOT_PASSWORD'],
        },
        docker_url='unix://var/run/docker.sock',
        network_mode='youtube_my_network',
        mount_tmp_dir=False,
        auto_remove='success',
    )

    upload_task >> transform_task
