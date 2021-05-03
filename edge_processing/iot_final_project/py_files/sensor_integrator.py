# This module is to register a new sensor connected to rapsbery PI.
# Whenever new sensor is connected to the system it automatically gives UUID to that sensor and start reading the data.
# @Author : Pramil Paudel

import RPi.GPIO as GPIO
import dht11
import time
from kafka import KafkaProducer
import json
import uuid


class PhysicalSensorScanner:
    status_detected = 'DETECTED'
    status_non_detected = 'NOT-DETECTED'
    file_delimeter="|"
    status_map = {}
    
        
    def scan_gpio_pins_and_check_for_status(self):
        GPIO.setmode(GPIO.BCM)
        for i in range(1,41):
            instance = dht11.DHT11(pin=i)
            result = instance.read()
            if result.is_valid():
                self.status_map[i] = self.status_detected
            else:
                self.status_map[i] = self.status_non_detected
        print("-----------------------")
        print("|PIN | DETECTION       ")
        print("-----------------------")

        for key in self.status_map:
            if key>=10:
                print("|", key , "|", self.status_map[key] ," |")
            else:
                print("|", key , " |", self.status_map[key] ," |")
        print("----------------------")
            
    def create_dynamic_uuid_for_current_active_sensor(self):
        return uuid.uuid4()
    
            
    def scan_sensor_network_and_update_config(self,config_location='../confg/active.config'):
        # Update self status_map
        self.scan_gpio_pins_and_check_for_status()
        # Read the old config and update only when there is change
        r_config_file = open(config_location,'r')
        #Removing header line and check
        old_data = r_config_file.readlines()[1:]
        r_config_file.close()
        ###############READING OLD DATA AND UPDATING #####################
        ndata = []
        for old_pin_data in old_data:
            #print(old_pin_data)
            # Update data only when new sensor is detected.
            # Config layout must match with following defination
            
            odata = old_pin_data.split(self.file_delimeter) 
            opin_number = odata[0]
            odetection = odata[1]
            ostatus = odata[2]
            ouuid = odata[3] 
            # Check current status_map
            #print(opin_number)
            n_detection = self.status_map.get(int(opin_number))
            #print(n_detection)
            if(n_detection != None and n_detection != odetection):
                odetection = n_detection
                if n_detection == self.status_non_detected:
                    ouuid = ""+"\n"
                if n_detection == self.status_detected:
                    ouuid = str(self.create_dynamic_uuid_for_current_active_sensor())+"\n"
            if odetection =="NOT-DETECTED":
                ostatus = "PASSIVE"
            nrow = str(opin_number) + self.file_delimeter + str(odetection) + self.file_delimeter + str(ostatus) + self.file_delimeter + str(ouuid)
            #print(nrow)
            ndata.append(str(nrow))
            
        ################### WRITING NEW UPDATED DATA ########################
        header_line = "#PIN_NUMBER|DETECTION|STATUS|UUID\n"
        w_config_file = open(config_location,'w')
        w_config_file.writelines(header_line)
        w_config_file.writelines(ndata)
        w_config_file.close()
        
#otesting = PhysicalSensorScanner()
#otesting.scan_sensor_network_and_update_config()