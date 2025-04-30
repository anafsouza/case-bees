from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from ..src.api.fetch_breweries import BreweryAPIClient
from ..src.processing.bronze_layer_writer import BronzeLayerWriter
from ..src.processing.silver_layer_writer import SilverLayerTransformer
from ..src.processing.gold_layer_aggregator import GoldLayerAggregator

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="brewery_medallion_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 4, 28),
    schedule_interval="@daily",
    catchup=False,
    tags=["brewery", "medallion", "data-pipeline"]
) as dag:
    
    date_str = datetime.today().strftime('%Y/%m/%d')

    def run_bronze(**kwargs):
        output_path = f"s3a://case-bees/bronze/{date_str}/"
        client = BreweryAPIClient(output_path)
        breweries = client.fetch_all_breweries()
        
        writer = BronzeLayerWriter(bucket_name="case-bees")
        writer.write_raw_json(breweries)

    def run_silver(**kwargs):
        input_path = f"s3a://case-bees/bronze/{date_str}/"
        output_path = f"s3a://case-bees/silver/{date_str}/"
        transformer = SilverLayerTransformer(input_path, output_path)
        transformer.transform_and_write()

    def run_gold(**kwargs):
        input_path = f"s3a://case-bees/silver/{date_str}/"
        output_path = f"s3a://case-bees/gold/{date_str}"
        aggregator = GoldLayerAggregator(input_path, output_path)
        aggregator.aggregate_and_write()

    bronze_task = PythonOperator(
        task_id="bronze_layer_ingestion",
        python_callable=run_bronze,
    )

    silver_task = PythonOperator(
        task_id="silver_layer_transform",
        python_callable=run_silver,
    )

    gold_task = PythonOperator(
        task_id="gold_layer_aggregate",
        python_callable=run_gold,
    )

    bronze_task >> silver_task >> gold_task
