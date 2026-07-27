# Databricks notebook source
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
from src.extract.readers import *

# COMMAND ----------

create_catalog_and_schemas(CATALOG, [BRONZE_SCHEMA, SILVER_SCHEMA, GOLD_SCHEMA])


# COMMAND ----------

# MAGIC %md
# MAGIC ## Below are Validations - Tries

# COMMAND ----------

# spark.sql("SHOW CATALOGS").show()
# spark.sql("CREATE SCHEMA IF NOT EXISTS nyc_databricks.bronze")