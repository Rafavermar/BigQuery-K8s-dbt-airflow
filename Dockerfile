FROM python:3.9.13

from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta
import airflow

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 4),
    'catchup': False
}

with airflow.DAG(
        'dbt_dag',
        default_args=default_args,
        schedule_interval=timedelta(days=1),
        catchup=False,
) as dag:

    # KubernetesPodOperator task to execute dbt run
    migrate_data = KubernetesPodOperator(
        namespace='default',
        image='jrvm/dbt_bigquery:dbt-image',
        cmds=["dbt run"],
        # No need to specify --profiles-dir since it's in the default location
        arguments=["--project-dir", "/dbt"],
        name="dbt_transformations",
        task_id="dbt_transformations",
        get_logs=True
    )

