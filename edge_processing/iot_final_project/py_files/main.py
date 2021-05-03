from temperature_reader import TemperatureReader
from activate_deactivate_sensor import ActivateDeactivateSensor 
from sensor_integrator import PhysicalSensorScanner
from back_up_plan import BackUpPlan
from collections import deque
import json
import time

def write_data_to_a_file(time,temp,enable_backup):
    if enable_backup:
        file_for_backup = open('../data/data_collected_with_backup.csv','a')
        file_for_backup.writelines(str(time)+"|"+str(temp)+"\n")
        file_for_backup.close()
    else:
        file_without_backup = open('../data/data_collected_without_backup.csv','a')
        file_without_backup.writelines(str(time)+"|"+str(temp)+"\n")
        file_without_backup.close()

#create objects
oscanner = PhysicalSensorScanner()
oactivation = ActivateDeactivateSensor()
oreader = TemperatureReader()
bplan = BackUpPlan()
temp_que = deque()
# Main Algorithm
# Initialization 
# Scanning Physical Sensor Network
oscanner.scan_sensor_network_and_update_config()
#Activate one arbitary PIN
activation = False
PIN_START = 1 
while not activation and PIN_START<41:
    activation = oactivation.activate_sensor(PIN_START)
    PIN_START = PIN_START + 1
    
# Reading the data from this active sensor
current_active_sensor=0
ENABLE_BACKUP = True
while True :
    BACK_UP_PLAN = False
    RECOVERY_STRATEGY = False
    print("DATA PROCESSING AND READING CYCLE")
    current_active_sensor = oreader.current_active_sensor_pin()
    if current_active_sensor==0:
        print("PLEASE CONNECT AT LEAST ONE SENSOR !!")
        break
    
    print("THIS IS CURRENT ACTIVE SENSOR", str(current_active_sensor))
    current_data = oreader.read_data_from_sensor()
    data_dict = json.loads(current_data)

    print("THE TEMPERATURE READING IS : ", data_dict["temperature"])
    print("THE TIME OF THE READING IS : ", data_dict["timestamp"])
    # Writing a condition when a backup sensor is to be activated
    
    temp_time_pair = {}
    temp = data_dict["temperature"]
    
    # Calling backup module
    backup_plan = bplan.return_back_up_plan(temp,temp_que)
    # Approximate Backup plan activation time is 10s
    print("THE CALCULATED BACKUP STRATEGY >>> ", backup_plan)
    #BACKUP PLAN
    if(ENABLE_BACKUP and backup_plan=="BACKUP"):
        BACK_UP_PLAN = True
        oscanner.scan_sensor_network_and_update_config()
        back_up_sensor = oactivation.next_backup_sensor()
        print(back_up_sensor)
        if back_up_sensor==0 :
            print("NO BACKUP AVAILABLE RECOVERY STARTING")
            print(current_active_sensor)
            RECOVERY_STRATEGY = True
        else:
            print("BACKUP SENSOR DETECTED TIME TO START A BACKUP SENSOR !!")
            print(current_active_sensor)
            oactivation.deactivate_sensor(current_active_sensor)
            oactivation.activate_sensor(back_up_sensor)
    elif(ENABLE_BACKUP and backup_plan=="RECOVERY"):
        RECOVERY_STRATEGY = True
    else:
        temp_time_pair[data_dict["timestamp"]]=data_dict["temperature"]
        print(temp_time_pair)
        temp_que.append(temp_time_pair)
        
        
    if len(temp_que)>10:
        first_data_of_que = dict(temp_que.popleft())
        for key,value in first_data_of_que.items():
            print("SYNCING WITH CLOUD")
            write_data_to_a_file(key,value,ENABLE_BACKUP)
            
            
    if not BACK_UP_PLAN and not RECOVERY_STRATEGY:
        time.sleep(4)
    elif BACK_UP_PLAN and not RECOVERY_STRATEGY:
        time.sleep(2)
    else:
        time.sleep(3)
    

#print(TemperatureReader.current_active_sensor)
