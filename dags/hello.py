from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'rafaverama',
    'start_date': datetime(2024, 0o3, 0o4),
    'catchup': False
}

dag = DAG(
    'First_K8s',
    default_args = default_args,
    schedule = timedelta(days=1)
)

t1 = BashOperator(
    task_id = 'first_k8s',
    bash_command ='echo "first_k8s"',
    dag = dag
)


t2 = BashOperator(
    task_id = 'rvm',
    bash_command ='echo "Rafa_Go ahead"',
    dag = dag
)

t1 >> t2