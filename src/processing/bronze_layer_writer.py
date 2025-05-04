import json
import boto3
from typing import List, Dict
from ..utils.logs import Logger


class BronzeLayerWriter:
    """
    Responsible for persisting raw data to the Bronze layer (S3).
    """

    def __init__(self, bucket_name: str, base_prefix: str = "bronze"):
        self.logger = Logger(name="bronze_layer_writer").get_logger()
        self.bucket = bucket_name
        self.prefix = base_prefix
        self.s3 = boto3.client("s3")

    def write_raw_json(self, data: List[Dict]):
        """
        Save raw JSON data to S3 as a JSON Lines file.

        Args:
            data (List[Dict]): List of brewery data from the API.
        """
        if not data:
            self.logger.warning("No data provided to write to Bronze layer.")
            return


        file_key = f"{self.prefix}/brewery_raw.jsonl"

        try:
            jsonl_data = "\n".join([json.dumps(item) for item in data])
            self.s3.put_object(Bucket=self.bucket, Key=file_key, Body=jsonl_data.encode("utf-8"))
            self.logger.info(f"Successfully wrote raw data to s3://{self.bucket}/{file_key}")

        except Exception as e:
            self.logger.exception("Failed to write raw data to the Bronze layer.")

