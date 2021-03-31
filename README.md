## Authors
`PRAMIL PAUDEl $ KAMALA GAJUREl`

## PORJECT SUMMARY 
- This project is titled as `Prediction on Streaming data from IOT`.
- Edge devices synchronize the sensor data to `Apache Kafka` using `Kafka Producer API`.
- Data from `Apache-Kafka-Stream` is consumed by `Apache-Spark-Streaming` using `pyspark`.
- The report generated from `pyspark` will be written in some `database`
- The `database data` is then Displayed in some beautiful Dashboard.
  
## Environment Setting 
- install `Apache-Kafka` and configure the running `port` : by default its 9092.
- May need to run `Apache-Zookepper` too.
- install 'Apache-Spark' (no need to run resourse manager (no any FS)) and run in standalone mode.


##  Mocking Up producer API
- Run Apache Kafka in the standalone or distributed system.

## Sample running script
- `python3 sensor_1_tmp.py`
- `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 main/spark-streaming/demo.py.`

## Environment Setup:
- Run `sensor_1_tmp.py` using `python3 main/kafka/producer/sensor_1_tmp.py`
- Run `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,mysql:mysql-connector-java:8.0.23 realtime_average_temperature.py`

## Check RUNNING JOBS In 
`http://localhost:4040/jobs/`


## SAMPLE pyspark OUTPUT

```` -------------------------------------------
Batch: 15
-------------------------------------------
+---------+-------------------+-------------------+---------------+
|device_id|       window_start|         window_end|avg_temperature|
+---------+-------------------+-------------------+---------------+
|        3|2019-10-01 10:20:00|2019-10-01 10:40:00|          15.75|
+---------+-------------------+-------------------+---------------+

-------------------------------------------
Batch: 16
-------------------------------------------
+---------+-------------------+-------------------+---------------+
|device_id|       window_start|         window_end|avg_temperature|
+---------+-------------------+-------------------+---------------+
|        3|2019-10-01 10:20:00|2019-10-01 10:40:00|      17.578125|
+---------+-------------------+-------------------+---------------+

-------------------------------------------
Batch: 17
-------------------------------------------
+---------+-------------------+-------------------+------------------+
|device_id|       window_start|         window_end|   avg_temperature|
+---------+-------------------+-------------------+------------------+
|        3|2019-10-01 10:20:00|2019-10-01 10:40:00|19.191176470588236|
+---------+-------------------+-------------------+------------------ `