# Databricks notebook source
import sys
sys.path.append("/Workspace/NYC_TAXI")
import importlib, src.bootstrap.bootstrap
importlib.reload(src.bootstrap)
from src.bootstrap.bootstrap import *

# COMMAND ----------

bronze_trips_type = read_delta(BRONZE_TYPE_DELTA)
silver_trips_type = bronze_trips_type
silver_trips_type.show(vertical=True)


# COMMAND ----------

bronze_trips = read_delta(BRONZE_TRIPS_DELTA)
before = bronze_trips.count()
print(f"Bronze trips: {before:,}")

# COMMAND ----------

bronze_zone = read_delta(BRONZE_ZONE_DELTA)
silver_zone = split_zone_names(bronze_zone)
silver_zone.select("Zone", "Zone1", "Zone2").show(10, truncate=False)

# COMMAND ----------

silver_trips = (bronze_trips
    .transform(remove_invalid_trips)
    .transform(deduplicate_trips)
    .transform(add_date_columns)
    .transform(add_audit_columns))

silver_trips = filter_to_year(silver_trips, 2023)

after = silver_trips.count()
print(f"Silver trips: {after:,} ({before - after:,} rejected)")

# COMMAND ----------

write_delta(silver_trips, SILVER_TRIPS_DELTA, f"{CATALOG}.{SILVER_SCHEMA}.trips")
write_delta(silver_zone, SILVER_ZONE_DELTA, f"{CATALOG}.{SILVER_SCHEMA}.zones")
write_delta(silver_trips_type, SILVER_TYPES_DELTA, f"{CATALOG}.{SILVER_SCHEMA}.trip_types")

# COMMAND ----------

# silver_zone = split_zone_names(bronze_zone)
# silver_zone.select("Zone", "Zone1", "Zone2").show(10, truncate=False)

# COMMAND ----------

# bronze_trips  = read_delta(BRONZE_TRIPS_DELTA)

# before = bronze_trips .count()
# clean = remove_invalid_trips(bronze_trips )
# after = clean.count()



# COMMAND ----------

# print(f"before: {before:,}")
# print(f"after: {after:,}")

# COMMAND ----------

# bronze_trips.filter(col('trip_distance') <= 0).count()
# bronze_trips.filter(col("fare_amount") < 0).count()
# bronze_trips.filter(col("passenger_count") == 0).count()

# COMMAND ----------

# before = bronze_trips.count()

# deduped = deduplicate_trips(bronze_trips)
# after = deduped.count()

# print(f"before:  {before:,}")
# print(f"after:   {after:,}")
# print(f"removed: {before - after:,}")

# COMMAND ----------

# dupes = bronze_trips.groupBy("VendorID", "lpep_pickup_datetime", "lpep_dropoff_datetime",
#              "PULocationID", "DOLocationID") \
#                  .count() \
#                      .filter(col("count") > 1)

# print(f"duplicate groups: {dupes.count():,}")
# # print(f"dupes: "); dupes.orderBy(col("PULocationID"),col("VendorID")).show(250)