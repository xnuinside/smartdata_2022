from prefect import flow, task, get_run_logger

run_count = 0


@task(retries=100, retry_delay_seconds=5)
def sensor():
    global run_count
    run_count += 1
    get_run_logger().info(f"Run number {run_count}")
    # here must be your sensor logic:
    #  query to DB, check the file, etc
    
    condition_met = False
    if not condition_met:
        raise Exception("Oh no! Need to continue wait!")
    return


@flow
def sensor_flow():
    return sensor()


if __name__ == "__main__":
    result = sensor_flow()
