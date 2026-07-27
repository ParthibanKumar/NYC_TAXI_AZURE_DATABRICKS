# Databricks notebook source
import sys
sys.path.append("/Workspace/NYC_TAXI")
import importlib, src.bootstrap.bootstrap
importlib.reload(src.bootstrap)
from src.bootstrap.bootstrap import *

# COMMAND ----------

silver_trips = read_delta(SILVER_TRIPS_DELTA)
silver_zone = read_delta(SILVER_ZONE_DELTA)

print(f"trips: {silver_trips.count():,}")
print(f"zones: {silver_zone.count():,}")

# COMMAND ----------

daily = daily_summary(silver_trips)
print(f"{daily.count()} rows")
daily.show(10)

# COMMAND ----------

by_zone = zone_summary(silver_trips, silver_zone)
print(f"{by_zone.count()} rows")
by_zone.show(15, truncate=False)

# COMMAND ----------

hourly = hourly_summary(silver_trips)
hourly.show(24)

# COMMAND ----------

write_delta(daily, GOLD_DAILY_DELTA, f"{CATALOG}.{GOLD_SCHEMA}.daily_summary")
write_delta(by_zone, GOLD_ZONE_DELTA, f"{CATALOG}.{GOLD_SCHEMA}.zone_summary")
write_delta(hourly, GOLD_HOURLY_DELTA, f"{CATALOG}.{GOLD_SCHEMA}.hourly_summary")