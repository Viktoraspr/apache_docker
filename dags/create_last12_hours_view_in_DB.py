from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.database.db_management import DBManagement

default_args = {
    'owner': 'Viktoras',
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}


def send_API_request():
    """
    Scraps CV Online page
    """
    print('Creating view in DB')
    table = DBManagement()
    table.create_last_12_hours()
    print('View is created')


with DAG(
    dag_id="Creating_view_'prices_last_12'",
    default_args=default_args,
    description="Creates views in DB",
    start_date=datetime(2023, 11, 14, 0),
    schedule_interval='@once',
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='send_API_request',
        python_callable=send_API_request,
    )

    task1
