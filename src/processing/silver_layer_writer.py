from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from ..utils.logs import Logger


class SilverLayerTransformer:
    """
    Responsible for transforming raw JSON data into Parquet format, partitioned by state.
    """

    def __init__(self, bronze_path: str, silver_path: str):
        self.logger = Logger(name="silver_layer_writer").get_logger()
        self.bronze_path = bronze_path
        self.silver_path = silver_path
        self.spark = self._create_spark_session()

    def _create_spark_session(self) -> SparkSession:
        """
        Creates and configures a SparkSession for local or distributed execution.
        """
        return SparkSession.builder \
            .appName("BrewerySilverLayer") \
            .getOrCreate()

    def transform_and_write(self):
        """
        Reads raw JSON data from S3, applies transformations,
        and writes it as Parquet, partitioned by 'state'.
        """
        try:
            self.logger.info(f"Reading raw data from: {self.bronze_path}")
            df = self.spark.read.json(self.bronze_path)

            self.logger.info("Performing basic transformations...")
            df_cleaned = df.filter(col("state").isNotNull()) \
                           .dropDuplicates(["id"])

            self.logger.info(f"Writing transformed data to: {self.silver_path}")
            df_cleaned.write.mode("overwrite") \
                .partitionBy("state") \
                .parquet(self.silver_path)

            self.logger.info("Successfully wrote Silver layer parquet data.")

        except Exception as e:
            self.logger.exception("Failed to transform or write data to Silver layer.")
