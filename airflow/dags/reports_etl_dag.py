from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from clickhouse_driver import Client

def load_test_reports():
    client = Client(host='clickhouse')
    client.execute("CREATE DATABASE IF NOT EXISTS reports")
    client.execute("""
        CREATE TABLE IF NOT EXISTS reports.user_reports (
            user_id String,
            report_date Date,
            total_actions UInt32,
            avg_latency_ms Float32
        ) ENGINE = MergeTree()
        ORDER BY (user_id, report_date)
    """)

    # Вставляем тестовые данные для всех пользователей
    client.execute("""
        INSERT INTO reports.user_reports VALUES
        ('b2c9a60f-3189-4508-a915-ae75b81f4ee5', '2025-12-26', 200, 75.3),
        ('418c277e-cbb9-4574-94fb-a70024d0fa0f', '2025-12-26', 150, 82.7)
    """)
    print("Test reports loaded into ClickHouse")

default_args = {
    'owner': 'bionicpro',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'reports_etl_dag',
    default_args=default_args,
    description='Load test reports into ClickHouse',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 12, 26),
    catchup=False,
)

load_task = PythonOperator(
    task_id='load_test_reports',
    python_callable=load_test_reports,
    dag=dag,
)