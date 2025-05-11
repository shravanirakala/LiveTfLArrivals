from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from utils.kafka_utils import produce_to_kafka

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    'tfl_api_to_kafka',
    default_args=default_args,
    description='Fetch TfL data and send to Kafka',
    schedule_interval='*/30 * * * *',
    catchup=False,
    max_active_runs=1,
    tags=['kafka', 'tfl']
) as dag:
    produce_task = PythonOperator(
        task_id='produce_to_kafka',
        python_callable=produce_to_kafka,
        execution_timeout=timedelta(minutes=2)
    )