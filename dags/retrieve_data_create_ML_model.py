from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.metals.live_metal import Metal
from src.ml.model import Model

default_args = {
    'owner': 'Viktoras',
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}


def send_api_request():
    """
    Scraps CV Online page
    """
    print('Scrapping cv online page and inserting in DB')
    metal = Metal()
    metal.run()
    print('Data injected in DB')


def create_ML_model():
    model = Model()
    # dag dag dag
    model.run("model1")


with DAG(
    dag_id='Retrieve_data_and_create_ML_model',
    default_args=default_args,
    description="Live metal data injection and ML module creator",
    start_date=datetime(2023, 11, 14, 0),
    schedule_interval='@hourly',
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='send_api_request',
        python_callable=send_api_request,
    )

    task2 = PythonOperator(
        task_id='create_ML_model',
        python_callable=create_ML_model,
    )

    task1 >> task2
