from collections import deque
import pmdarima as pm

# Backup Plan runs with three major flags strategies


class BackUpPlan():
    
    generic_and_obvious_outlier = False
    accidental_yet_true_outlier = False
    history_trend_based_outlier = False
    
    current_reading = 0.0
    
    
    def return_back_up_plan(self,temp,data_deque):
        self.generic_and_obvious_outlier = False
        self.accidental_yet_true_outlier = False
        self.history_trend_based_outlier = False
        self.re_assessment_needed(temp,data_deque)
        self.calculate_moving_average(temp,data_deque)
    
        if self.generic_and_obvious_outlier:
            return "BACKUP"
        elif self.history_trend_based_outlier:
            return "RECOVERY"
        elif self.accidental_yet_true_outlier:
            return "BACKUP"
        else:
            return "OKAY"
        
    def re_assessment_needed(self,temp,data_deque):
        if float(temp)==999:
            self.generic_and_obvious_outlier = True
        else:
            self.calculate_moving_average(temp,data_deque)
    
    def calculate_moving_average(self,temp,data_deque):
        # Read data from all data deque
        room_temp = 25
        data = [room_temp]
        if len(data_deque)>=10:
            for i in range(0,len(data_deque)):
                for key, value in dict(data_deque[i]).items():
                    data.append(float(value))
            model = pm.auto_arima(data,seasonal=False, m=0)
            prediction = model.predict(1)
            print("ARIMA PREDICTION FOR LATEST 10 VALID DATA :: ",str(prediction))
            # Adding 10% tolerance
            predicted_temp = float(prediction[0])
            if float(temp) < 0.9*predicted_temp or float(temp) > 1.1*predicted_temp:
                self.history_trend_based_outlier = True
            elif float(temp) > 0.9*predicted_temp or float(temp)< 1.1*predicted_temp:
                self.generic_and_obvious_outlier = False
                self.accidental_yet_true_outlier = False
                self.history_trend_based_outlier = False
            else:
                self.accidental_yet_true_outlier = True

            
    def testP(self):
        model = pm.auto_arima([25,45,25,24,67,8,12,12,13,12,14,15],seasonal=False, m=1)
        prediction = model.predict(1)
        print(float(prediction[0]))
        print(prediction)
        
#test = BackUpPlan()
#test.testP()