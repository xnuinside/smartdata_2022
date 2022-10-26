from prefect import flow, get_run_logger, task


@task
def summary(result: int):
    get_run_logger().info(result)
    return sum(result)
    
@task
def calculate(name: str):
    get_run_logger().info(f"Hello {name}!")

@flow
def fibonachi(number: int, count: int = 5):
    result = calculate.map(number for i in range(count))
    return summary(result)


if __name__ == "__main__":
    fibonachi(number=3, tasks=5)
