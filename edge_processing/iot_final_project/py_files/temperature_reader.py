import RPi.GPIO as GPIO
import dht11
import time
from kafka import KafkaProducer
import json
#from activate_deactivate_sensor import ActivateDeactivateSensor

# initialize GPIO 
#GPIO.setwarning(False)

class TemperatureReader():
    active_map = {}
    odata_map  = {}
    header = ""
    file_delimeter = "|"
    current_active_sensor = 0

    def load_config_file(self):
        # Read the old config and update only when there is change
        r_config_file = open('../confg/active.config','r')
        #Removing header line and check
        file_data = r_config_file.readlines()
        self.header = file_data[:1]
        old_data = file_data[1:]
        r_config_file.close()
        ###############READING OLD DATA ####################
        for old_pin_data in old_data:
            odata = old_pin_data.split("|")
            self.odata_map[int(odata[0])] = str(old_pin_data)
            self.active_map[int(odata[0])] = str(odata[2])
            
    def load_current_active_sensor(self):
        self.load_config_file()
        for key in self.active_map:
            if self.active_map[key]=="ACTIVE":
                self.current_active_sensor=int(key)
    
    def current_active_sensor_pin(self):
        self.load_current_active_sensor()
        return self.current_active_sensor
     
    
    def read_data_from_sensor(self):
        self.load_current_active_sensor()
        print("CURRENT DATA IS BEING READ FROM SENSOR CONNECTED IN GPIO_PIN ::: " , str(self.current_active_sensor))
        GPIO.setmode(GPIO.BCM)
        data = {}
        temp = 999
        humidity = 999
        instance = dht11.DHT11(pin=int(self.current_active_sensor))
        result = instance.read()
        if result.is_valid():
            temp, humidity = result.temperature, result.humidity
        
        print("DETAILS ::: ")
        
        odata = self.odata_map[int(self.current_active_sensor)].split("|")
        opin_number = odata[0]
        odetection = odata[1]
        ostatus =odata[2]
        ouuid = odata[3]
        
        print("\n PIN_NUMBER:: ", opin_number, "\n DETECTION :: ", odetection, "\n STATUS :: ", ostatus, "\n UUID :: ", ouuid)
        
        data["device_id"]=ouuid.strip()
        time_data = time.localtime()
        time_string = time.strftime("%Y-%m-%d, %H:%M:%S",time_data)
        data["timestamp"]=time_string
        data["temperature"]=str(temp)
        data["humidity"]=str(humidity)
        json_data=json.dumps(data)
        return str(json_data)

#reader = TemperatureReader()
#print(reader.read_data_from_sensor())
        
