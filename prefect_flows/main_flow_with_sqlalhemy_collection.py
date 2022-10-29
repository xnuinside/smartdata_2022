from prefect import flow, get_run_logger, task
from prefect_sqlalchemy import DatabaseCredentials, AsyncDriver
from prefect_sqlalchemy.database import sqlalchemy_execute
from datetime import datetime
# for the flow I create a 'test' table test_data
# create table test_data(id int, date date, condition boolean)
# insert into test_data(id, date, condition) values(1, '2022-10-29', true)
# and we need to wait insert line with required date - if it exists
# when we start the flow
# but  based on field 'condition' we decide that to do next

run_count = 0

def get_db_creds() -> DatabaseCredentials:
    return DatabaseCredentials(
        driver=AsyncDriver.POSTGRESQL_ASYNCPG,
        # !!! never-never ever do this - is just a tutorial sample!!!!
        # keep your secrets private!
        username="postgres",
        password="postgres",
        database="orion",
    )


@task(retries=100, retry_delay_seconds=5)
def wait_for_db_record(sqlalchemy_credentials: DatabaseCredentials):
    global run_count
    run_count += 1
    # and it will return always None :D I think prefect_sqlalchemy does not work correct
    condition = sqlalchemy_execute(
        "SELECT * from test_data WHERE date = :date_now ;",
        sqlalchemy_credentials,
        params={"date_now": datetime.utcnow().date().isoformat()}
    )
    
    condition_met = condition is not None
    if not condition_met:
        raise Exception("Oh no! Need to continue wait!")

@flow
def get_data(sqlalchemy_credentials: DatabaseCredentials) -> str:
    # and it will return always None :D I think prefect_sqlalchemy does not work correct
    condition = sqlalchemy_execute(
        "SELECT * from test_data",
        sqlalchemy_credentials
    )
    get_run_logger().info(f"Result from DB {condition}")
    return condition


@task
def process_or_skip_func(condition: str):
    if condition == False:
        return 'skip'
    return 'process'

@task
def if_skip_do_something():
    get_run_logger().info(f"Task {if_skip_do_something.__name__}")


@task
def if_not_skip_do_something_func():
    get_run_logger().info(f"Task {if_not_skip_do_something_func.__name__}")


@task
def report_the_finish(result: str):
    get_run_logger().info(f"Task {report_the_finish.__name__}")


@flow(task_runner=SequentialTaskRunner())
def db_data_process_flow():
    sqlalchemy_credentials = get_db_creds()
    wait_for_db_record(sqlalchemy_credentials)
    data = get_data(sqlalchemy_credentials)
    status = process_or_skip_func(data)
    if status == 'skip':
        val = if_skip_do_something()
        report_the_finish(val)
    else:
        val = if_not_skip_do_something_func()
        report_the_finish(val)


if __name__ == "__main__":
    db_data_process_flow()
