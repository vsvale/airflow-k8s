import yfinance
from datetime import  timedelta
from airflow.decorators import dag, task_group, task
from airflow.utils.dates import days_ago
from airflow.macros import ds_add
from astro import sql as aql
from astro.files import File

default_args = {
    'owner': 'vinicius da silva vale',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'email': ['viniciusdvale@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'max_active_run': 1,
    'depends_on_past':False}

description = "DAG to get stock data"

TICKERS = ['AAPL','MSFT','GOOG','TSLA']


@dag(schedule='@daily', default_args=default_args,catchup=False,
tags=['alura','stock','yfinance','s3','k8s'],description=description)
def alura_stock_k8s():


    @task()
    def get_crypto_values(ticker):
        df = yfinance.Ticker(ticker).history(
            period="1d", 
            interval="1h",
            start=days_ago(1),
            end=days_ago(0),
            prepost=True,
            )
        return df

    
    for ticker in TICKERS:
        load_to_S3 = aql.export_file(
        task_id=f"t_load_df_to_s3_{ticker}",
        input_data=get_crypto_values(ticker),
        output_file=File(
            path=f"s3://lakehouse/stocks/{ticker}/{ticker}.csv",
            conn_id="minio",
        ),
        if_exists="replace"
    )

dag = alura_stock_k8s()