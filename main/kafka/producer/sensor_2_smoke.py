import time, pickle
from kafka import KafkaProducer
import json


if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers="localhost:9092")

    with open('../../../json/sensor_json/smoke_sensor.json.json') as f:
        data = json.load(f)


    # todo modify the json data and send
    for x in range(1000):
        producer.send("test", bytes(str(data), 'utf-8'))
        # adding some delay (sensor frequency ).
        time.sleep(1)