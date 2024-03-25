from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 31),
}

dag = DAG('kerberos_renew_2', default_args=default_args, schedule_interval='@once')

t1 = BashOperator(
    task_id='renew_ticket53',
    bash_command='/opt/airflow/dags/renew_ticket.sh ',  # Correct path to your script
    network_mode='host',
    dag=dag,
)
