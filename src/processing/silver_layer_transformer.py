import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim
from .bronze_layer_writer import BronzeLayerWriter
from ..utils.logs import Logger
from ..utils.s3_renaming_files import move_and_rename_parquet_file


class SilverLayerTransformer:
    """
    Responsible for transforming raw JSON data into Parquet format, partitioned by country.
    """

    def __init__(
        self, 
        bronze_path: str = "s3a://case-bees/bronze/brewery_raw.jsonl", 
        # silver_path: str = ""
    ):
        self.logger = Logger(name="silver_layer_writer").get_logger()
        self.bronze_path = bronze_path
        self.silver_path = "s3a://case-bees/silver/"
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

    def transform(self):
        """
        Reads raw JSON data from S3, applies transformations,
        and writes it as Parquet, partitioned by 'state'.
        """
        try:
            self.logger.info(f"Reading raw data from: {self.bronze_path}")
            df = self.spark.read.json(self.bronze_path)

            self.logger.info("Performing basic transformations...")
            df_cleaned = df.filter(col("country").isNotNull()).dropDuplicates(["id"])
            df_cleaned = df_cleaned.withColumn("country", trim(df_cleaned["country"]))
            return df_cleaned

        except Exception as e:
            self.logger.exception("Failed to transform data to Silver layer.")

    def write_data(self):
        try:
            df_silver = self.transform()
            countries = [row['country'] for row in df_silver.select("country").distinct().collect()]
            
            self.logger.info(f"Writing transformed data to: {self.silver_path}")
            
            bucket = "case-bees"
            tmp_prefix = "tmp/export_breweries"
            for country in countries:
                df_country = df_silver.filter(df_silver.country == country).coalesce(1)

                tmp_path = f"s3a://{bucket}/{tmp_prefix}/{country}/"
                final_key = f"silver/{country}/breweries.parquet"
                # Writes the file temporarily
                df_country.write.mode("overwrite").parquet(tmp_path)
                
    
                move_and_rename_parquet_file(
                    bucket="case-bees",
                    tmp_prefix=tmp_prefix,
                    final_key=final_key
                )


            self.logger.info("Successfully wrote Silver layer parquet data.")
            
        except Exception as e:
            self.logger.exception("Failed to write data to Silver layer.")