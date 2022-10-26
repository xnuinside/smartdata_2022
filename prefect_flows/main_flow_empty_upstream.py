from prefect import flow, get_run_logger, task


@task
def wait_for_db_record():
    pass


@task
def get_data():
    pass


@task
def process_or_skip_func():
    pass

@task
def branch_on_skip_func():
    pass


@task
def if_skip_do_something():
    pass


@task
def if_not_skip_do_something_func():
    pass


@task
def report_the_finish():
    pass


@flow
def db_data_process_flow():
    wait_for_task = wait_for_db_record()
    get_data_task = get_data(
        upstream_tasks=[wait_for_task])
    process_or_skip_func_task = process_or_skip_func(
        upstream_tasks=[get_data_task])
    branch_on_skip_func_task = branch_on_skip_func(
        upstream_tasks=[process_or_skip_func_task])
    if_skip_do_something_task = if_skip_do_something(
        upstream_tasks=[branch_on_skip_func_task])
    if_not_skip_do_something_func_task = if_not_skip_do_something_func(
        upstream_tasks=[if_skip_do_something_task])
    report_the_finish(
        upstream_tasks=[if_not_skip_do_something_func_task])


if __name__ == "__main__":
    db_data_process_flow()
