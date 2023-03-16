from datetime import datetime
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.decorators import task

with DAG(dag_id="example_dynamic_task_mapping", start_date=datetime(2023, 3, 15)) as dag:

    @task
    def add_one(x: int):
        return x + 1

    @task
    def sum_it(values):
        total = sum(values)
        print(f"Total was {total}")

    added_values = add_one.expand(x=[1, 2, 3])
    sum_it(added_values)