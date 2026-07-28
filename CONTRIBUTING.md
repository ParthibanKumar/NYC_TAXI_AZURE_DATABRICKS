# Setup & Run Guide

This project runs on Azure. To reproduce it end to end you need an Azure subscription, an ADLS Gen2 storage account, and a Databricks workspace. The source data is public, so no data files are stored in this repo.

## 1. Source data

Download the 2023 NYC TLC **green** taxi Parquet files (one per month) plus the zone and trip-type lookups from the [TLC trip record page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). In this project the monthly files are ingested automatically by Data Factory from the public CloudFront endpoint, so you do not need to download them by hand — the ADF pipeline does it.

## 2. Storage (ADLS Gen2)

Create a storage account with **hierarchical namespace enabled** and three containers:

```
bronze/   raw landings + bronze delta tables
silver/   cleaned delta tables
gold/     aggregate delta tables
```

Recommended account settings: LRS redundancy, Hot access tier, public network access enabled (for a learning setup), TLS 1.2, anonymous blob access **off**. SFTP and NFSv3 stay off.

## 3. Ingestion (Azure Data Factory)

Import the pipeline from `datafactory/arm_template.json` (ADF Studio → Manage → ARM template → Import). It contains:

- An HTTP linked service to the TLC endpoint and an ADLS Gen2 linked service to your `bronze` container.
- A pipeline with a **ForEach** over the 12 months (items built as a padded month array), containing a **Copy Data** activity that pulls `green_tripdata_2023-MM.parquet` into `bronze/`.

Update the linked-service connection strings to point at your own storage account, then publish and trigger.

## 4. Keyless access (Access Connector + Unity Catalog)

This is the piece that makes storage access secretless.

1. Create an **Access Connector for Azure Databricks** in the same region as your workspace.
2. On the storage account → **Access Control (IAM)** → assign **Storage Blob Data Contributor** to the connector's managed identity.
3. In Databricks → **Catalog → External Data → Credentials** → create a **Storage Credential** (Azure Managed Identity) referencing the connector's Resource ID.
4. Create an **External Location** for each container:
   - `abfss://bronze@<account>.dfs.core.windows.net/`
   - `abfss://silver@<account>.dfs.core.windows.net/`
   - `abfss://gold@<account>.dfs.core.windows.net/`
5. Use **Test connection** on each — Read / Write / List should pass.

## 5. Import the code into Databricks

Clone this repo into your Databricks workspace via **Repos** (Workspace → Repos → Add Repo), or import the `notebooks/` and `src/` folders manually into a workspace folder named `NYC_TAXI`.

The notebooks add the project root to the path so the `src` package is importable:

```python
import sys
sys.path.append("/Workspace/NYC_TAXI")
from src.bootstrap.bootstrap import *
```

Update `src/config/project_config.py` with your own storage account name and catalog name before running.

## 6. Run order

Run the notebooks in sequence:

| Notebook | Does |
|---|---|
| `01_catalog_creation` | Creates the schemas under your Unity Catalog catalog |
| `02_bronze_ingest` | Reads raw Parquet + lookups, writes Bronze Delta tables |
| `03_silver_transform` | Cleans, deduplicates, enriches; writes Silver |
| `04_gold_aggregate` | Builds daily / zonal / hourly aggregates; writes Gold |

## 7. Verify

```sql
SELECT COUNT(*) FROM <catalog>.bronze.trips;      -- ~787k
DESCRIBE HISTORY <catalog>.silver.trips;          -- Delta transaction log
SELECT * FROM <catalog>.gold.daily_summary ORDER BY trip_date LIMIT 10;
```

## Notes on structure

- **Notebooks orchestrate; `src/` holds logic.** Cleaning and aggregation are plain functions taking a DataFrame and returning one, so they can be unit-tested without a notebook.
- **Config and schemas are centralised** in `src/config` and `src/schema` — change the storage account or target year in one place.
- **Module edits require a reload** in an active notebook session (`importlib.reload(...)`) or a detach/reattach, because Python caches imports.

## Security

There are **no credentials in this codebase** — access is via managed identity. If you fork this, do not add account keys or service-principal secrets to notebooks, even commented out. Use the Access Connector pattern above.
