from prefect import flow, task


@task
def say_hello(name: str):
    """Print a greeting message."""
    print(f"Hello, {name}!")


@flow
def etl_pipeline():
    """Main ETL pipeline flow."""
    say_hello("Prefect Cloud")
