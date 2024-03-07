from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


def get_data(**kwargs):
    import requests
    import pandas as pd
    url = (
        'https://raw.githubusercontent.com/Rafavermar/FootballRVMDataEngineering/master/data/output.csv')
    response = requests.get(url)

    if response.status_code == 200:
        df = pd.read_csv(url, header=None,
                         names=['rank', 'stadium', 'capacity', 'region', 'country', 'city', 'images', 'home_team'])

        # convert DataFrame to JSON from xcom
        json_data = df.to_json(orient='records')

        kwargs['ti'].xcom_push(key='data', value=json_data)
    else:
        raise Exception(f'Failed to get data, HTTP status code: {response.status_code}')


def preview_data(**kwargs):
    import json
    import pandas as pd
    output_data = kwargs['ti'].xcom_pull(key='data', task_ids='get_data')

    if output_data:
        output_data = json.loads(output_data)
    else:
        raise ValueError('No data received from XCom')

    # create a Dataframe
    df = pd.DataFrame(output_data)

    print(df[['rank', 'stadium']].head(10))


default_args = {
    'owner': 'rafaverama',
    'start_date': datetime(2024, 0o3, 0o4),
    'catchup': False
}

dag = DAG(
    'dbt_TEST',
    default_args=default_args,
    schedule=timedelta(days=1)
)

get_data_from_url = PythonOperator(
    task_id='get_data',
    python_callable=get_data,
    dag=dag
)

preview_data_from_url = PythonOperator(
    task_id='preview_data',
    python_callable=preview_data,
    dag=dag
)

get_data_from_url >> preview_data_from_url
