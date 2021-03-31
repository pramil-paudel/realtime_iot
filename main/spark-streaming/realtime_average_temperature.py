# -- This file can be checked to see the realtime processing of temperature data from temperature sensor
# -- The code calculated the average temperature and print in console.


from pyspark.sql import SparkSession
from pyspark.sql.functions import asc, desc, col, from_json, to_timestamp, window
from pyspark.sql.types import StructType, LongType, DoubleType, StringType
from kafka import KafkaConsumer
from pyspark.sql import functions as F

if __name__ == "__main__":
    spark = SparkSession.builder.appName("StreamingPipeline").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    kafka_topic_input = "temperature_and_humidity"
    consumer = KafkaConsumer(kafka_topic_input, bootstrap_servers="192.168.0.23:9092")

    df = (
        spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", "192.168.0.23:9092")
            .option("subscribe", kafka_topic_input)
            .load()
    )

    df_str = df.selectExpr("CAST(value AS STRING) as value")

    schema = (
        StructType()
            .add("device_id", LongType())
            .add("timestamp", StringType())
            .add("temperature", DoubleType())
            .add("humidity", DoubleType())
    )

    df_parsed = df_str.select(from_json(df_str.value, schema).alias("data"))

    df_formatted = df_parsed.select(
        col("data.device_id").alias("device_id"),
        col("data.timestamp").alias("timestamp"),
        col("data.temperature").alias("temperature")
    )

    df_time_stamp = df_formatted.withColumn(
        "timestamp", to_timestamp(df_formatted.timestamp, "yyyy-MM-dd HH:mm:ss"),
    )

    df_window = (
        df_time_stamp.withWatermark("timestamp", "20 minutes")
            .groupBy(window(df_time_stamp.timestamp, "20 minutes"), df_time_stamp.device_id)
            .avg("temperature")
    )

    df_final = df_window.select(
        "device_id",
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("avg(temperature)").alias("avg_temperature"),
    ).orderBy(asc("device_id"), asc("window_start"))

    query_console = (
        df_final.writeStream.outputMode("complete").format("console").start()
    )
    #

    def write_data_to_mysql(df,epoch_id):
        df.write.format('jdbc').options(
            url='jdbc:mysql://localhost:3306/iot',
            driver='com.mysql.jdbc.Driver',
            dbtable='temperature',
            user='root',
            password='').mode('append').save()

    query = df_final.writeStream.outputMode("complete").foreachBatch(write_data_to_mysql).start()

    query.awaitTermination()

    query_console.awaitTermination()
