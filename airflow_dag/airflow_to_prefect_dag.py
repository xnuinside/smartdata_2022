from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.exceptions import AirflowSkipException


def if_not_skip_do_something_func():
   return 'non skip'


def if_skip_do_something_func(context):
   return 'skip'


def process_or_skip_func(context):
   task_instance = context['ti']
   xcom_value = task_instance.xcom_pull(task_ids='get_data')
   if xcom_value == False:
      raise AirflowSkipException
   else:
      return True


def branch_on_skip_func(context):
   task_instance = context['ti']
   xcom_value = task_instance.xcom_pull(task_ids='process_or_skip')
   if xcom_value == 'skip':
      return 'if_skip_do_something'
   else:
      return 'if_not_skip_do_something_func'

""" 
   here can be any normal table and select for example by date
   
   Create table for DAG in DB (I use same DB that in Airflow)
   
   create table trigger_table(
      run_flag boolean, 
      id int
   )

"""

with DAG(dag_id="airflow_to_prefect_dag", 
         start_date=datetime(2019, 11, 28),
         schedule_interval="@daily") as dag:
         wait_for_db_record = SqlSensor(
            # here can be any normal table and select for example by date
            sql="SELECT run_flag from trigger_table where id > 1000",
            task_id="wait_for_db_record",
            conn_id="postgres_default"
            )
         get_data = PostgresOperator(
            task_id="get_data",
            postgres_conn_id="postgres_default",
            sql="SELECT run_flag from trigger_table where id > 1000;"
         )
         process_or_skip = PythonOperator(
            python_callable=process_or_skip_func,
            task_id="process_or_skip",
            )
         branch_on_skip = BranchPythonOperator(
            python_callable=branch_on_skip_func,
            task_id="branch_on_skip",
            trigger_rule="none_failed"
            )
         if_skip_do_something = PythonOperator(
            python_callable=if_skip_do_something_func,
            task_id="if_skip_do_something",
         )
         if_not_skip_do_something = PythonOperator(
            python_callable=if_not_skip_do_something_func,
            task_id="if_not_skip_do_something"
            )
         report_the_finish = DummyOperator(
            task_id="report_the_finish"
            )

         wait_for_db_record >> get_data >> process_or_skip >> branch_on_skip >> [
            if_skip_do_something, if_not_skip_do_something] >> report_the_finish
