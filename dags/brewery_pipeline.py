from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from ..src.api.fetch_breweries import BreweryAPIClient
from ..src.processing.bronze_layer_writer import BronzeLayerWriter
from ..src.processing.silver_layer_transformer import SilverLayerTransformer
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
    

    def run_bronze():
        client = BreweryAPIClient()
        breweries = client.fetch_all_breweries()
        
        writer = BronzeLayerWriter(bucket_name="case-bees")
        writer.write_raw_json(breweries)

    def run_silver():
        transformer = SilverLayerTransformer()
        transformer.write_data()

    def run_gold():
        aggregator = GoldLayerAggregator()
        aggregator.write_data()


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
