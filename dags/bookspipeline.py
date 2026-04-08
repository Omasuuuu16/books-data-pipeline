from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import sys

def run_scrape():
    sys.path.insert(0, '/usr/local/airflow/include')
    from scrape_books import scrape_books
    scrape_books()

with DAG(
    dag_id="books_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    scraping_task = PythonOperator(
        task_id="scrape_books",
        python_callable=run_scrape
    )

    dbt_seed_task = BashOperator(
        task_id="dbt_seed",
        bash_command="cd /usr/local/airflow/books_project && dbt seed --profiles-dir /usr/local/airflow/books_project"
    )

    dbt_run_task = BashOperator(
        task_id="dbt_run",
        bash_command="cd /usr/local/airflow/books_project && dbt run --profiles-dir /usr/local/airflow/books_project"
    )

    scraping_task >> dbt_seed_task >> dbt_run_task