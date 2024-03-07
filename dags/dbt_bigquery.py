import airflow

from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime, timedelta

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

    # KubernetesPodOperator task para ejecutar dbt run
    migrate_data = KubernetesPodOperator(
        namespace='default',
        image='your_docker_hub_username/your_repository:your_tag',  # Cambia esto con la ruta de tu imagen en Docker Hub
        cmds=["dbt", "run"],
        arguments=[
            "--project-dir", "./<project_dir>", "--profiles-dir", "./<project_dir>/profiles"
        ],
        name="dbt_transformations",
        task_id="dbt_transformations",
        get_logs=True
    )

