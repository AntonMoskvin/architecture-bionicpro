from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import psycopg2
from clickhouse_driver import Client
import requests

def extract_telemetry():
    conn = psycopg2.connect(
        host="db", user="...", password="...", dbname="..."
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, timestamp, action_type, latency_ms
        FROM telemetry
        WHERE timestamp >= %(yesterday)s
    """, {"yesterday": (datetime.now() - timedelta(days=1)).date()})
    rows = cur.fetchall()
    conn.close()
    return rows

def extract_users():
    # Предположим: user_id → prosthesis_id хранится в атрибутах Keycloak
    # Или можно читать из Bitrix API
    return {"user1": "prosthesisA", "user2": "prosthesisB"}

def transform_and_load(**context):
    telemetry = context['task_instance'].xcom_pull(task_ids='extract_telemetry')
    users = extract_users()

    # Агрегация
    agg = {}
    for user_id, ts, action, latency in telemetry:
        if user_id not in agg:
            agg[user_id] = {"actions": 0, "total_latency": 0, "movements": set()}
        agg[user_id]["actions"] += 1
        agg[user_id]["total_latency"] += latency
        agg[user_id]["movements"].add(action)

    # Запись в ClickHouse
    client = Client(host='clickhouse')
    report_date = (datetime.now() - timedelta(days=1)).date()
    data = []
    for user_id, stats in agg.items():
        data.append((
            user_id,
            report_date,
            stats["actions"],
            stats["total_latency"] / stats["actions"],
            list(stats["movements"])
        ))
    client.execute("INSERT INTO reports.user_reports VALUES", data)

with DAG(
        'reports_etl',
        schedule_interval='@daily',
        start_date=datetime(2025, 12, 1),
        catchup=False,
) as dag:

    t1 = PythonOperator(task_id='extract_telemetry', python_callable=extract_telemetry)
    t2 = PythonOperator(task_id='load', python_callable=transform_and_load)

    t1 >> t2