from dagster import job, op, ScheduleDefinition, Definitions, asset, sensor, RunRequest, resource
import subprocess
import sys

@op
def scrape_telegram_data_op():
    subprocess.run([sys.executable, "src/scrape_telegram.py"], check=True)

@op
def load_raw_to_postgres_op():
    subprocess.run([sys.executable, "src/load_to_postgres.py"], check=True)

@op
def run_dbt_transformations_op():
    subprocess.run(["dbt", "run"], check=True)

@op
def run_yolo_enrichment_op():
    subprocess.run([sys.executable, "src/yolo_detection.py"], check=True)

@op
def run_load_image_detections_op():
    subprocess.run([sys.executable, "src/load_image_detections.py"], check=True)

@asset
def my_asset():
    # Example asset logic: just returns a string
    return "Asset loaded successfully!"

@resource
def my_resource(_):
    # Example resource logic: returns a simple dictionary
    return {"resource_key": "resource_value"}

@job
def telegram_analytics_pipeline():
    scrape_telegram_data_op()
    load_raw_to_postgres_op()
    run_dbt_transformations_op()
    run_yolo_enrichment_op()
    run_load_image_detections_op()

@sensor(job=telegram_analytics_pipeline)
def my_sensor(context):
    # Example sensor logic: always triggers a run
    yield RunRequest(run_key=None, run_config={})

telegram_analytics_schedule = ScheduleDefinition(
    job=telegram_analytics_pipeline,
    cron_schedule="0 2 * * *",  # Runs daily at 2am
)

defs = Definitions(
    jobs=[telegram_analytics_pipeline],
    schedules=[telegram_analytics_schedule],
    assets=[my_asset],
    sensors=[my_sensor],
    resources={"my_resource": my_resource},
)