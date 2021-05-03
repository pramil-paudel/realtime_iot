import RPi.GPIO as GPIO
import dht11
import time
from kafka import KafkaProducer
import json

# initialize GPIO 
#GPIO.setwarning(False)

def send_data_to_kafka(data_1):
    producer = KafkaProducer(bootstrap_servers="192.168.0.23:9092")
    producer.send("temperature_and_humidity",bytes(str(data_1),'utf-8'))


def read_data_from_sensor():
    instance = dht11.DHT11(pin=14)
    result = instance.read()
    if result.is_valid():
        return result.temperature, result.humidity
    else:
        print("THERE OCCUR AN ERROR WHILE READING THE TEMP AND HUMIDITY")
        return 999, 999

def create_json_object():
    while(1):
        GPIO.setmode(GPIO.BCM)
        data = {}
        temp, humidity = read_data_from_sensor()
        data["device_id"]=5
        data["timestamp"]="2020-10-01 10:33:00"
        data["temperature"]=temp
        data["humidity"]=humidity
        json_data=json.dumps(data)
        send_data_to_kafka(json_data)
        print(json_data)
        time.sleep(1)
        GPIO.cleanup()


create_json_object()
