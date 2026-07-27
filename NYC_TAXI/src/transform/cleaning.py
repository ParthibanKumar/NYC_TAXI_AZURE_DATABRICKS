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

def remove_invalid_trips(df):
    return (
        df.filter(col("lpep_pickup_datetime").isNotNull()) \
            .filter(col("lpep_dropoff_datetime") > col("lpep_pickup_datetime")) \
                        .filter(col("trip_distance") > 0) \
                            .filter(col("fare_amount") >= 0) \
                                .filter(col("passenger_count") > 0)
    )

def deduplicate_trips(df):
    """Remove exact duplicate trips."""
    return df.dropDuplicates([
        "VendorID", "lpep_pickup_datetime", "lpep_dropoff_datetime",
        "PULocationID", "DOLocationID",
    ])

def add_date_columns(df):
    """Add date columns for partitioning and grouping."""
    return (df
            .withColumn("trip_date", to_date("lpep_pickup_datetime"))
            .withColumn("pickup_year", year("lpep_pickup_datetime"))
            .withColumn("pickup_month", month("lpep_pickup_datetime"))
            )

def add_audit_columns(df):
    """Add ingestion metadata."""
    return df.withColumn("ingested_at", current_timestamp())

def filter_to_year(df, target_year):
    """Keep only trips actually within the target year."""
    return df.filter(col("pickup_year") == target_year)


def split_zone_names(df):
    """Split the Zone column on '/' into Zone1 and Zone2."""
    return (df
        .withColumn("Zone1", trim(split(col("Zone"), "/")[0]))
        .withColumn("Zone2", trim(get(split(col("Zone"), "/"), 1))))




