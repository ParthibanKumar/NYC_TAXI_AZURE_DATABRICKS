from pyspark.sql.types import  StructType, StructField, IntegerType, StringType, TimestampType, DoubleType, TimestampNTZType, LongType

ZONE_SCHEMA = StructType([
    StructField('Location', IntegerType(), False),
    StructField("Borough", StringType(), True),
    StructField("Zone", StringType(), True),
    StructField("service_zone", StringType(), True),
])

TYPE_SCHEMA = StructType([
    StructField("trip_type", IntegerType(), False),
    StructField("description", StringType(), True),
])

TAXI_DATA_SCHEMA = StructType([
    StructField("VendorID", LongType(), True),
    StructField("lpep_pickup_datetime", TimestampNTZType(), True),
    StructField("lpep_dropoff_datetime", TimestampNTZType(), True),
    StructField("store_and_fwd_flag", StringType(), True),
    StructField("RatecodeID", DoubleType(), True),
    StructField("PULocationID", LongType(), True),
    StructField("DOLocationID", LongType(), True),
    StructField("passenger_count", DoubleType(), True),
    StructField("trip_distance", DoubleType(), True),
    StructField("fare_amount", DoubleType(), True),
    StructField("extra", DoubleType(), True),
    StructField("mta_tax", DoubleType(), True),
    StructField("tip_amount", DoubleType(), True),
    StructField("tolls_amount", DoubleType(), True),
    StructField("ehail_fee", DoubleType(), True),
    StructField("improvement_surcharge", DoubleType(), True),
    StructField("total_amount", DoubleType(), True),
    StructField("payment_type", DoubleType(), True),
    StructField("trip_type", DoubleType(), True),
    StructField("congestion_surcharge", DoubleType(), True),

])