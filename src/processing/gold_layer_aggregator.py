from pyspark.sql import SparkSession
from ..utils.logs import Logger


class GoldLayerAggregator:
    """
    Responsible for creating analytical aggregations from the Silver layer.
    """

    def __init__(self, silver_path: str, gold_path: str):
        self.logger = Logger(name="gold_layer_aggregator").get_logger()
        self.silver_path = silver_path
        self.gold_path = gold_path
        self.spark = self._create_spark_session()

    def _create_spark_session(self) -> SparkSession:
        return SparkSession.builder \
            .appName("BreweryGoldLayer") \
            .getOrCreate()

    def aggregate_and_write(self):
        """
        Performs aggregation by brewery type and state, and saves result as Parquet.
        """
        try:
            self.logger.info(f"Reading cleaned data from: {self.silver_path}")
            df = self.spark.read.parquet(self.silver_path)

            self.logger.info("Performing aggregations...")
            aggregated_df = df.groupBy("state", "brewery_type").count() \
                               .withColumnRenamed("count", "brewery_count")

            self.logger.info(f"Writing aggregated data to: {self.gold_path}")
            aggregated_df.write.mode("overwrite").parquet(self.gold_path)

            self.logger.info("Successfully wrote Gold layer aggregated data.")

        except Exception as e:
            self.logger.exception("Failed to aggregate or write data to Gold layer.")
