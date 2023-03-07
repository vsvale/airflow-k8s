import yfinance
from datetime import  timedelta
from airflow.decorators import dag, task_group, task
from airflow.utils.dates import days_ago
from airflow.macros import ds_add


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

TICKERS = ['AAPL','MSFT','GOOG','TSLA']



@dag(schedule='@daily', default_args=default_args,catchup=False,
tags=['alura','stock','yfinance','s3','k8s'],description=description)
def alura_stock_k8s():
    @task()
    def get_history(ticker, ds=None, ds_nodash=None):
        df = yfinance.Ticker(ticker).history(
        period="1d", 
        interval="1h",
        start=ds_add(ds, -1),
        end=ds,
        prepost=True,
        )
        print(df)
    @task()
    def get_crypto_dag():
        for ticker in TICKERS:
            get_history.override(task_id=ticker)(ticker)
    get_crypto_dag()
dag = alura_stock_k8s()