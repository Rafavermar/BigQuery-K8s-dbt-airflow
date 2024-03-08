from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 3, 4),
}

with DAG(
    'dbt_full_workflow',
    default_args=default_args,
    description='A DAG to run dbt tasks including run, seed, and test',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    dbt_run = KubernetesPodOperator(
        namespace='default',
        image='jrvm/dbt_bigquery:dbt-image',
        cmds=["dbt", "run"],
        arguments=["--project-dir", "/dbt_bigquery_main", "--profiles-dir", "/dbt_bigquery_main"],
        name="dbt_run",
        task_id="dbt_run",
        get_logs=True,
        image_pull_policy='Always',
        is_delete_operator_pod=True,
    )

    dbt_seed = KubernetesPodOperator(
        namespace='default',
        image='jrvm/dbt_bigquery:dbt-image',
        cmds=["dbt", "seed"],
        arguments=["--project-dir", "/dbt_bigquery_main", "--profiles-dir", "/dbt_bigquery_main"],
        name="dbt_seed",
        task_id="dbt_seed",
        get_logs=True,
        image_pull_policy='Always',
        is_delete_operator_pod=True,
    )

    dbt_test = KubernetesPodOperator(
        namespace='default',
        image='jrvm/dbt_bigquery:dbt-image',
        cmds=["dbt", "test"],
        arguments=["--project-dir", "/dbt_bigquery_main", "--profiles-dir", "/dbt_bigquery_main"],
        name="dbt_test",
        task_id="dbt_test",
        get_logs=True,
        image_pull_policy='Always',
        is_delete_operator_pod=True,
    )

    dbt_run >> dbt_seed >> dbt_test
