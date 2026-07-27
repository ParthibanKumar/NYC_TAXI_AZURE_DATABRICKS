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


# def write_delta(df, path, table_name, mode="overwrite"):
#     """Write a DataFrame as a Delta table and register it in the catalog."""
#     (df.write
#         .format("delta")
#         .mode(mode)
#         .option("overwriteSchema", "true")
#         .save(path))

#     spark = df.sparkSession
#     spark.sql(f"CREATE TABLE IF NOT EXISTS {table_name} USING DELTA LOCATION '{path}'")

#     print(f"Wrote {table_name} to {path}")


def write_delta(df, path, table_name, mode="overwrite"):
    """Write a DataFrame as an external Delta table."""
    (df.write.format("delta") \
        .mode(mode) \
            .option("path", path) \
                .option("overwriteSchema", True) \
                    .saveAsTable(table_name))
    print(f"{table_name}: {df.count():,} written")