import time
from kafka import KafkaProducer
import json

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers="localhost:9092")

    with open('../../../json/sensor_json/temp_sensor.json') as f:
        data = json.load(f)


    # todo : modify the JSON data and send (need to be modified to create prediction modeling)
    for x in range(1000):
        producer.send("test", bytes(str(data), 'utf-8'))
        # loading a bit slow
        time.sleep(1)