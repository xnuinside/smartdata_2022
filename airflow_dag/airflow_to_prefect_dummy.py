from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator


with DAG(dag_id="airflow_to_prefect_dag_dummy", 
         start_date=datetime(2019, 11, 28),
         schedule_interval="@daily") as dag:
         wait_for_db_record = DummyOperator(
            task_id = "wait_for_db_record"
         )
         get_data = DummyOperator(
            task_id = "get_data"
            )
         process_or_skip = DummyOperator(
            task_id = "process_or_skip"
         )
         branch_on_skip = DummyOperator(
            task_id = "branch_on_skip"
         )
         if_skip_do_something = DummyOperator(
            task_id = "if_skip_do_something"
         )
         if_not_skip_do_something = DummyOperator(
            task_id = "if_not_skip_do_something"
         )
         report_the_finish = DummyOperator(
            task_id = "report_the_finish"
         )

         wait_for_db_record >> get_data >> process_or_skip >> branch_on_skip >> [
            if_skip_do_something, if_not_skip_do_something] >> report_the_finish
