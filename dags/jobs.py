from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from uuid import uuid4
import os


default_args = {
    'owner'                 : 'airflow',
    'description'           : 'Data pipeline for immo eliza',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 11, 21),
    'email_on_failure'      : False,
    'email_on_retry'        : False,
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5)
}

with DAG('immo-eliza-pipeline', default_args=default_args, schedule_interval="30 * * * *", catchup=False) as dag:

    pipeline_id = str(uuid4())

    start_dag = DummyOperator(
        task_id='start_dag'
        )

    end_dag = DummyOperator(
        task_id='end_dag'
        )        
        
    t1 = DockerOperator(
        task_id='scraping',
        image='airflow_tutorial_scraper:latest',
        container_name='task___scraper',
        api_version='auto',
        auto_remove=True,
        # command="/bin/sleep 30",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        environment={
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "STORAGE_CONTAINER": os.getenv("STORAGE_CONTAINER"),
            "PIPELINE_ID": pipeline_id
        }
        )

    t2 = DockerOperator(
        task_id='training',
        image='airflow_tutorial_training:latest',
        container_name='task___training',
        api_version='auto',
        auto_remove=True,
        # command="/bin/sleep 30",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        
        environment= {
            "AZURE_CONNECTION_STRING": os.getenv("AZURE_CONNECTION_STRING"),
            "STORAGE_CONTAINER": os.getenv("STORAGE_CONTAINER"),
            "PIPELINE_ID": pipeline_id
        }
        )

    t3 = BashOperator(
        task_id='print_done',
        bash_command='echo "All done!"'
    )

    start_dag >> t1 
    
    t1 >> t2 >> t3

    t3 >> end_dag