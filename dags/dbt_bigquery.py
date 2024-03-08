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
        'dbt_dag_test',
        default_args=default_args,
        schedule_interval=timedelta(days=1),
        catchup=False,
) as dag:
    test_command = KubernetesPodOperator(
        namespace='default',
        image='jrvm/dbt_bigquery:dbt-image',
        cmds=["ls"],  # Comando a ejecutar
        arguments=["-lah", "/dbt"],  # Argumentos del comando, lista el contenido del directorio /dbt
        name="test_command",
        task_id="test_command",
        get_logs=True,
        is_delete_operator_pod=False,
        security_context={'runAsUser': 0},  # Ejecutar como root si es necesario
    )
