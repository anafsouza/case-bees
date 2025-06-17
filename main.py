from src.api.fetch_breweries import BreweryAPIClient
from src.processing.bronze_layer_writer import BronzeLayerWriter
from src.processing.silver_layer_transformer import SilverLayerTransformer
from src.processing.gold_layer_aggregator import GoldLayerAggregator


def main():

    client = BreweryAPIClient()
    breweries = client.fetch_all_breweries()

    writer = BronzeLayerWriter(bucket_name="case-bees")
    writer.write_raw_json(breweries)

    transformer = SilverLayerTransformer()
    transformer.write_data()

    aggregator = GoldLayerAggregator()
    aggregator.write_data()

if __name__ == "__main__":
    main()
    
