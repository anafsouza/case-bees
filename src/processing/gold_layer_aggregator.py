import os
from pyspark.sql import SparkSession
from ..utils.logs import Logger
from ..utils.s3_renaming_files import move_and_rename_parquet_file


class GoldLayerAggregator:
    """
    Responsible for creating analytical aggregations from the Silver layer.
    """

    def __init__(
        self, 
        silver_path: str = "s3a://case-bees/silver/*/breweries.parquet", 
    ):
        self.logger = Logger(name="gold_layer_aggregator").get_logger()
        self.silver_path = silver_path
        self.gold_path = "s3://case-bees/gold/"
        self.spark = self._create_spark_session()

    def _create_spark_session(self) -> SparkSession:
        """
        Creates and configures a SparkSession for local or distributed execution.
        """
        return SparkSession.builder \
                .appName("Gold Layer") \
                .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.11.901") \
                .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
                .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
                .config("spark.hadoop.fs.s3a.access.key", os.environ["AWS_ACCESS_KEY_ID"]) \
                .config("spark.hadoop.fs.s3a.secret.key", os.environ["AWS_SECRET_ACCESS_KEY"]) \
                .getOrCreate()

    def aggregate(self):
        """
        Performs aggregation by brewery type and state, and saves result as Parquet.
        """
        try:
            self.logger.info(f"Reading cleaned data from: {self.silver_path}")
            df = self.spark.read.parquet(self.silver_path)

            self.logger.info("Performing aggregations...")
            aggregated_df = df.groupBy("country", "brewery_type") \
                   .count() \
                   .withColumnRenamed("count", "brewery_count")

            return aggregated_df

        except Exception as e:
            self.logger.exception("Failed to aggregate data to Gold layer.")

    def write_data(self):
        try:
            df_gold = self.aggregate()
            self.logger.info(f"Writing aggregated data to: {self.gold_path}")


            bucket = "case-bees"
            tmp_prefix = "tmp/breweries_agg/"
            tmp_path = f"s3a://{bucket}/{tmp_prefix}/"
            final_key = "gold/breweries_by_type_and_country.parquet"
            df_gold.coalesce(1).write.mode("overwrite").parquet(tmp_path)

            move_and_rename_parquet_file(
                bucket="case-bees",
                tmp_prefix=tmp_prefix,
                final_key=final_key
            )
            self.logger.info("Successfully wrote Gold layer aggregated data.")
            
        except Exception as e:
            self.logger.exception("Failed to write data to Gold layer.")
