Open Brewery API

      ↓
[ Task: fetch_brewery_data ]
      ↓

Bronze Layer
(Save raw JSON)

      ↓
[ Task: transform_and_partition_silver ]

      ↓
Silver Layer
(Save Parquet, partition by location)

      ↓
[ Task: aggregate_gold_layer ]

      ↓
Gold Layer
(Aggregated count per brewery type and state)
