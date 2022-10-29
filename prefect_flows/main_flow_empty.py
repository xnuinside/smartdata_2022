from prefect import flow, get_run_logger, task


@task
def wait_for_db_record():
    get_run_logger().info(f"Task {wait_for_db_record.__name__}")


@task
def get_data():
    get_run_logger().info(f"Task {get_data.__name__}")


@task
def process_or_skip_func(data: str):
    get_run_logger().info(f"Task {process_or_skip_func.__name__}")

@task
def if_skip_do_something():
    get_run_logger().info(f"Task {if_skip_do_something.__name__}")


@task
def if_not_skip_do_something_func():
    get_run_logger().info(f"Task {if_not_skip_do_something_func.__name__}")


@task
def report_the_finish(result: str):
    get_run_logger().info(f"Task {report_the_finish.__name__}")


@flow
def db_data_process_flow():
    wait_for_db_record()
    data = get_data()
    status = process_or_skip_func(data)
    if status == 'skip':
        val = if_skip_do_something()
        report_the_finish(val)
    else:
        val = if_not_skip_do_something_func()
        report_the_finish(val)


if __name__ == "__main__":
    db_data_process_flow()
