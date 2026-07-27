STORAGE_ACCOUNT = "nyctaxi2023dev"

BRONZE = f"abfss://bronze@{STORAGE_ACCOUNT}.dfs.core.windows.net"
SILVER = f"abfss://silver@{STORAGE_ACCOUNT}.dfs.core.windows.net"
GOLD = f"abfss://gold@{STORAGE_ACCOUNT}.dfs.core.windows.net"

TRIP_DATA_PATH = f"{BRONZE}/trips2023data/trip-data"
TRIP_ZONE_PATH = f"{BRONZE}/trip_zone"
TRIP_TYPE_PATH = f"{BRONZE}/trip_type"

TRIP_FILE_PATTERN = "green_tripdata_2023-{month:02d}.parquet"
MONTHS = range(1, 13)

BRONZE_TRIPS_DELTA = f"{BRONZE}/delta/trips"
BRONZE_ZONE_DELTA = f"{BRONZE}/delta/zones"
BRONZE_TYPE_DELTA = f"{BRONZE}/delta/trip_types"

SILVER_TRIPS_DELTA = f"{SILVER}/delta/trips"
SILVER_ZONE_DELTA = f"{SILVER}/delta/zones"
SILVER_TYPES_DELTA = f"{SILVER}/delta/trip_types"

GOLD_DAILY_DELTA = f"{GOLD}/delta/daily_summary"
GOLD_ZONE_DELTA = f"{GOLD}/delta/zone_summary"
GOLD_HOURLY_DELTA = f"{GOLD}/delta/hourly_summary"

CATALOG = "nyc_databricks"
BRONZE_SCHEMA = "bronze"
SILVER_SCHEMA = "silver"
GOLD_SCHEMA = "gold"

