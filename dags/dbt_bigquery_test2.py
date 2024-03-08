from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 4),
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_debug_dag',
    default_args=default_args,
    description='A simple DAG to run dbt debug',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    dbt_debug = KubernetesPodOperator(
        namespace='default',
        image='jrvm/dbt_bigquery:dbt-image',
        cmds=["dbt", "debug"],
        arguments=["--project-dir", "/dbt", "--profiles-dir", "/dbt"],
        name="dbt-debug",
        task_id="dbt_debug_task",
        get_logs=True,
        is_delete_operator_pod=True,
        security_context={'runAsUser': 0},
    )
