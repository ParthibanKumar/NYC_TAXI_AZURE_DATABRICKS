# Databricks notebook source
import sys
sys.path.append("/Workspace/NYC_TAXI")
import importlib, src.bootstrap.bootstrap
importlib.reload(src.bootstrap)
from src.bootstrap.bootstrap import *

# COMMAND ----------

df_trips = read_trip_data()
df_zone = read_trip_zone()
df_type = read_trip_type()

# COMMAND ----------

write_delta(df_trips, BRONZE_TRIPS_DELTA, f"{CATALOG}.{BRONZE_SCHEMA}.trips")
write_delta(df_zone, BRONZE_ZONE_DELTA, f"{CATALOG}.{BRONZE_SCHEMA}.zones")
write_delta(df_type, BRONZE_TYPE_DELTA, f"{CATALOG}.{BRONZE_SCHEMA}.trip_types")


# COMMAND ----------

# MAGIC %md
# MAGIC ## # The following items are intended for practice and testing purposes only. Reviewers, please disregard them.

# COMMAND ----------

# print(dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get())
# print(os.listdir("/Workspace/NYC_TAXI")
# print(sys.path)
# print(ZONE_SCHEMA)

# COMMAND ----------

# application_client_id="960faaf2-66b6-436f-a1ae-1659b5f22116"
# client_secret="8af03c1e-da4f-4ad9-8d0f-5daf36d2fd51"
# directory_id="79c71e42-7358-4b0e-88c7-2139c60ba7c4"
# storage_account_name="nyctaxi2023dev"

# COMMAND ----------

# MAGIC %md
# MAGIC abfss :// bronze @ nyctaxi2023dev .dfs.core.windows.net /
# MAGIC   │         │           │              │                │
# MAGIC   │         │           │              │                └─ path within container
# MAGIC   │         │           │              └─ ADLS Gen2 endpoint suffix
# MAGIC   │         │           └─ your storage account name
# MAGIC   │         └─ container name
# MAGIC   └─ protocol/driver

# COMMAND ----------

# dbutils.fs.ls("abfss://bronze@nyctaxi2023dev.dfs.core.windows.net/trips2023data/trip-data/")
# dbutils.fs.ls("abfss://bronze@nyctaxi2023dev.dfs.core.windows.net/trip_type")
# dbutils.fs.ls("abfss://bronze@nyctaxi2023dev.dfs.core.windows.net/trip_zone")
# print(spark.catalog.currentCatalog())

# COMMAND ----------

# df_trip_type = spark.read.format("csv").option("header",True).schema(TYPE_SCHEMA).load(TRIP_TYPE_PATH)

# df_trip_zone = spark.read.format("csv").schema(ZONE_SCHEMA).option("header",True).load(TRIP_ZONE_PATH)

# print(f"{df_trip_type.show(vertical=True)}, Total_Count={df_trip_type.count()} ")
# print(f"{df_trip_zone.show(500, truncate=False)} , Total_count={df_trip_zone.count()}")

# df_trip_zone.select(df_trip_zone["Zone"]).show()

# df_trip_zone = df_trip_zone \
#     .withColumn("Zone 1", trim(get(split(col("Zone"), "/"),0))) \
#     .withColumn("Zone 2", trim(get(split(col("Zone"), "/"),1)))

# display(df_trip_zone)

# COMMAND ----------

# base = "abfss://bronze@nyctaxi2023dev.dfs.core.windows.net/trips2023data/trip-data/"
# for m in ["01", "03"]:
#     print("=== month", m)
#     spark.read.parquet(base + f"green_tripdata_2023-{m}.parquet").printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Datafarme Loading

# COMMAND ----------

# dfs = []
# for m in range(1, 13):
#     p = f"{TRIP_DATA_PATH}/{TRIP_FILE_PATTERN.format(month=m)}"
#     d = spark.read.parquet(p).withColumn("ehail_fee", col("ehail_fee").cast("double"))
#     dfs.append(d)

# df_trip_data = dfs[0]
# for d in dfs[1:]:
#     df_trip_data = df_trip_data.unionByName(d, allowMissingColumns=True)

# print(f"{df_trip_data.count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validation Cell

# COMMAND ----------

# if df_trip_data.schema != TAXI_DATA_SCHEMA:
#     print("Schema differs from expected")


# actual = df_trip_data.schema
# expected = TAXI_DATA_SCHEMA

# print("In actual, not expected:")
# for f in actual.fields:
#     if f not in expected.fields:
#         print("  ", f)

# print("In expected, not actual:")
# for f in expected.fields:
#     if f not in actual.fields:
#         print("  ", f)


# actual = df_trip_data.schema
# expected = TAXI_DATA_SCHEMA

# print("same?", actual == expected)
# print("field count:", len(actual.fields), "vs", len(expected.fields))

# for a, e in zip(actual.fields, expected.fields):
#     if a != e:
#         print("DIFF:", a, "|", e)

# print(df_trip_data.schema)
