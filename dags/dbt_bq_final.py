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

    seed_data = KubernetesPodOperator(
        namespace='default',
        image='jrvm/dbt_bigquery:dbt-image',
        cmds=["dbt", "seed"],
        arguments=["--project-dir", "/dbt_bigquery_main", "--profiles-dir", "/dbt_bigquery_main", "--full-refresh"],
        name="dbt_seed",
        task_id="dbt_seed",
        get_logs=True,
        is_delete_operator_pod=False,
        image_pull_policy='Always',
        security_context={'runAsUser': 0},
    )

    migrate_data = KubernetesPodOperator(
        namespace='default',
        image='jrvm/dbt_bigquery:dbt-image',
        cmds=["dbt", "run"],
        arguments=["--project-dir", "/dbt_bigquery_main", "--profiles-dir", "/dbt_bigquery_main"],
        name="dbt_transformations",
        task_id="dbt_transformations",
        get_logs=True,
        is_delete_operator_pod=False,
        image_pull_policy='Always',
        security_context={'runAsUser': 0},
    )

    seed_data >> migrate_data