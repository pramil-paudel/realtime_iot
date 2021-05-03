# The purpose of the code is to read update and modify current active sensor 
#from sensor_integrator import PhysicalSensorScanner

class ActivateDeactivateSensor:
    active_map = {}
    odata_map  = {}
    detected_map = {}
    header = ""
    file_delimeter = "|"
    
    def returnSensorStatus(self,pin_number):
        self.load_config_file()
        #print(self.active_map)
        #print(self.odata_map)
        return str(self.active_map[pin_number])
        
    
    def deactivate_sensor(self,pin_number):
        self.load_config_file()
        if self.active_map[int(pin_number)] == "ACTIVE":
            odata = self.odata_map[int(pin_number)].split("|")
            opin_number = odata[0]
            odetection = odata[1]
            ostatus ="PASSIVE"
            ouuid = odata[3]
            nrow = str(opin_number) + self.file_delimeter + str(odetection) + self.file_delimeter + str(ostatus) + self.file_delimeter + str(ouuid)
            self.odata_map[int(pin_number)] = nrow      
        self.write_config_file()
        
    def activate_sensor(self,pin_number):
        activation = False
        self.load_config_file()
        if self.active_map[int(pin_number)] == "PASSIVE" or self.active_map[int(pin_number)] == "":
            odata = self.odata_map[int(pin_number)].split("|")
            opin_number = odata[0]
            odetection = odata[1]
            ostatus ="PASSIVE"
            if(odetection == "DETECTED"):
                ostatus ="ACTIVE"
                activation = True
            ouuid = odata[3]
            nrow = str(opin_number) + self.file_delimeter + str(odetection) + self.file_delimeter + str(ostatus) + self.file_delimeter + str(ouuid)
            self.odata_map[int(pin_number)] = nrow      
        self.write_config_file()        
        return activation                            
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
            self.detected_map[int(odata[0])] = str(odata[1])

        
    def write_config_file(self):
        w_config_file = open('../confg/active.config','w')
        w_config_file.writelines(self.header)
        for key in self.odata_map:
            w_config_file.writelines(self.odata_map[key])
        w_config_file.close()
                        
    def next_backup_sensor(self):
        self.load_config_file()
        BACK_UP = 0
        for i in range(1,41):
            if self.active_map[i]=="PASSIVE" and self.detected_map[i]=="DETECTED":
                return i
        return BACK_UP
        
#otesting = ActivateDeactivateSensor()
#otesting.deactivate_sensor(15)
#print(otesting.returnSensorStatus(14))