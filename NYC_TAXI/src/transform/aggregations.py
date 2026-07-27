from pyspark.sql import SparkSession
spark = SparkSession.getActiveSession()
from pyspark.sql.functions import *
from pyspark.sql.types import *
from functools import reduce
import sys
sys.path.append("/Workspace/NYC_TAXI")
import os
import importlib
import src.schema.project_schemas
import src.config.project_config
importlib.reload(src.schema.project_schemas)
from src.schema.project_schemas import *
from src.config.project_config import *


def daily_summary(df):
    return (df
        .groupBy("trip_date")
        .agg(
            count("*").alias("trip_count"),
            round(sum("total_amount"), 2).alias("total_revenue"),
            round(avg("fare_amount"), 2).alias("avg_fare"),
            round(avg("trip_distance"), 2).alias("avg_distance"),
        )
        .orderBy("trip_date"))
    

def zone_summary(trips, zones):
    """Pickups by borough and zone, joined to zone names."""
    return (trips
        .join(broadcast(zones), trips.PULocationID == zones.Location, "left")
        .groupBy("Borough", "Zone")
        .agg(
            count("*").alias("pickup_count"),
            round(sum("total_amount"), 2).alias("total_revenue"),
            round(avg("trip_distance"), 2).alias("avg_distance"),
        )
        .orderBy(col("pickup_count").desc()))


def hourly_summary(df):
    """Trips by hour of day."""
    return (df
        .withColumn("pickup_hour", hour("lpep_pickup_datetime"))
        .groupBy("pickup_hour")
        .agg(
            count("*").alias("trip_count"),
            round(avg("fare_amount"), 2).alias("avg_fare"),
        )
        .orderBy("pickup_hour"))