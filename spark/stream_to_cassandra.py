from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType
import logging
from cassandra_schema import create_cassandra_schema

SCHEMA = StructType([
    StructField("id", StringType()),
    StructField("tfl_id", StringType()),
    StructField("mode_name", StringType()),
    StructField("station_name", StringType()),
    StructField("platform_name", StringType()),
    StructField("towards", StringType()),
    StructField("timestamp", StringType()),
    StructField("time_to_station", StringType()),
    StructField("expected_arrival", StringType())
])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stream")


def main():
    
    logger.info("Spark session initializing...")
    spark = SparkSession.builder \
        .appName("KafkaToCassandra") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0," +
                "com.datastax.spark:spark-cassandra-connector_2.12:3.4.1") \
        .config("spark.cassandra.connection.host", "cassandra") \
        .config("spark.cassandra.auth.username", "cassandra") \
        .config("spark.cassandra.auth.password", "cassandra") \
        .getOrCreate()
    
    logger.info("Spark session created...")

    create_cassandra_schema()

    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "tfl_arrivals") \
        .option("startingOffsets", "earliest") \
        .load()

    # df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    # .writeStream \
    # .format("console") \
    # .option("truncate", False) \
    # .start() \
    # .awaitTermination()
    
    parsed_df = df.select(from_json(col("value").cast("string"), SCHEMA).alias("data")).select("data.*")

    final_df = parsed_df \
        .withColumn("timestamp", to_timestamp("timestamp")) \
        .withColumn("expected_arrival", to_timestamp("expected_arrival")) \
        .withColumn("time_to_station", col("time_to_station").cast("int"))

    final_df.writeStream \
        .format("org.apache.spark.sql.cassandra") \
        .option("checkpointLocation", "/tmp/checkpoint") \
        .option("keyspace", "tfl_arrivals") \
        .option("table", "ksx") \
        .start() \
        .awaitTermination()

if __name__ == "__main__":
    main()
