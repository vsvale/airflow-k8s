import yfinance
from datetime import  timedelta
from airflow.decorators import dag, task_group, task
from airflow.utils.dates import days_ago
from airflow.macros import ds_add
from astro import sql as aql


default_args = {
    'owner': 'vinicius da silva vale',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'email': ['viniciusdvale@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'max_active_run': 1}

description = "DAG to get stock data"



@dag(schedule='@daily', default_args=default_args,catchup=False,
tags=['alura','stock','yfinance','s3','k8s'],description=description)
def alura_stock_k8s():

    @task()
    def select_ticker():
        return ['AAPL','MSFT','GOOG','TSLA']

    @task()
    def get_crypto_values(ticker: str):
        return ticker

    @task()
    def consumer(arg):
        print(list(arg))


    crypto_values = get_crypto_values.expand(ticker = select_ticker())
    consumer(crypto_values)


dag = alura_stock_k8s()