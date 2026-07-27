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



def read_trip_data():
    """Read all 12 monthly parquet files and combine into one DataFrame."""
    dfs = []

    for m in range(1, 13):
        path = f"{TRIP_DATA_PATH}/{TRIP_FILE_PATTERN.format(month=m)}"
        df = spark.read.parquet(path)
        df = df.withColumn("ehail_fee", col("ehail_fee").cast("double"))
        dfs.append(df)

    combined = dfs[0]
    for df in dfs[1:]:
        combined = combined.unionByName(df, allowMissingColumns=True)

    return combined


def read_trip_zone():
    """Read the zone lookup CSV."""
    return (
        spark.read.format("csv") \
            .option("header",True) \
                .schema(ZONE_SCHEMA) \
                    .load(TRIP_ZONE_PATH)

    )

def read_trip_type():
    """Read the trip type lookup CSV."""
    return(
        spark.read.format("csv") \
            .option("header", True) \
                .schema(TYPE_SCHEMA) \
                    .load(TRIP_TYPE_PATH)
    )


def create_catalog_and_schemas(catalog, schemas):
    """Create the catalog and its schemas if they don't exist."""
    # spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
    for s in schemas:
        spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{s}")


def read_delta(path):
    """Read a Delta table by its storage path."""
    return spark.read.format("delta").load(path)