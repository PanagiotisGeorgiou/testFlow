from prefect import flow, task

@task
def say_hello(name: str):
    print(f"Hello, {name}!")

@flow
def etl_pipeline():
    say_hello("Prefect Cloud")

