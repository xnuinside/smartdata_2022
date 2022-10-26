import json

import pendulum

from airflow.decorators import dag, task

from airflow.utils.log.logging_mixin import LoggingMixin

log = LoggingMixin().log


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
)
def airflow_to_prefect_dag_task_flow():
    @task
    def wait_for_db_record():
        pass
    @task
    def get_data():
        pass
    @task
    def process_or_skip_func(data: str):
        pass
    @task
    def if_skip_do_something():
        pass

    @task.branch()
    def branch_on_skip():
        pass

    @task
    def if_not_skip_do_something_func():
        pass

    @task
    def report_the_finish():
        pass
    
    result = wait_for_db_record()
    data = get_data(result) 
    state = process_or_skip_func(data)
    branch_on_skip(state) >> [if_not_skip_do_something_func(), 
    if_skip_do_something()] >> report_the_finish()

airflow_to_prefect_dag_task_flow()