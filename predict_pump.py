import sys
import json
import time
import joblib
import threading
from datetime import datetime
from collections import deque

running = True

def listen_for_enter():
    global running
    input()
    running = False
    print("Stopping the program...")

# Load the ML model
model = joblib.load('best_model.joblib')

class SensorBuffer:
    def __init__(self, size=5):  # Average over last 5 readings
        self.buffer = deque(maxlen=size)
        
    def add_reading(self, value):
        self.buffer.append(value)
        
    def get_average(self):
        if not self.buffer:
            return 0
        return sum(self.buffer) / len(self.buffer)

def predict_pump_state(moisture_value):
    prediction = model.predict([[moisture_value]])
    return "on" if prediction[0] == 1 else "off"

def format_output(timestamp, farm1_data, farm1_pump_state, farm2_data, farm2_pump_state):
    return {
        "timestamp": timestamp,
        "sender1": farm1_data["sender"],
        "Farm1_moisture": farm1_data["moisture"],
        "Farm1_flow_meter": farm1_data["flow_meter"],
        "Farm1_pump_state": farm1_pump_state,
        "sender2": farm2_data["sender"],
        "Farm2_moisture": farm2_data["moisture"],
        "Farm2_flow_meter": farm2_data["flow_meter"],
        "Farm2_pump_state": farm2_pump_state
    }

if len(sys.stdin.readline()) > 1:
    input_data = sys.stdin.readline()
    data = json.loads(input_data)
    
    h1 = data['data']['h1']
    h3 = data['data']['h3']
    v_meter_2 = data['data']['V_Meter_2']
    v_meter_3 = data['data']['V_Meter_3']

    # Create sensor buffers for averaging readings
    farm1_buffer = SensorBuffer()
    farm2_buffer = SensorBuffer()

    # Define thresholds with buffer zones
    lower_threshold = 30
    upper_threshold = 90
    buffer_zone = 2  # 2% buffer to prevent oscillation

    # Keep track of previous states to prevent rapid switching
    prev_farm1_state = "off"
    prev_farm2_state = "off"

    try:
        while running:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            # Add new readings to buffers
            farm1_buffer.add_reading(h1)
            farm2_buffer.add_reading(h3)
            
            # Get averaged readings
            farm1_moisture = farm1_buffer.get_average()
            farm2_moisture = farm2_buffer.get_average()
            
            # Farm 1 control logic with ML model
            if prev_farm1_state == "off":
                farm1_should_turn_on = farm1_moisture < (lower_threshold - buffer_zone)
                model_prediction = predict_pump_state(farm1_moisture)
                farm1_pump_state = "on" if (farm1_should_turn_on and model_prediction == "on") else "off"
            else:  # previous state was "on"
                farm1_should_stay_on = farm1_moisture < (upper_threshold + buffer_zone)
                model_prediction = predict_pump_state(farm1_moisture)
                farm1_pump_state = "on" if (farm1_should_stay_on and model_prediction == "on") else "off"

            # Farm 2 control logic with ML model
            if prev_farm2_state == "off":
                farm2_should_turn_on = farm2_moisture < (lower_threshold - buffer_zone)
                model_prediction = predict_pump_state(farm2_moisture)
                farm2_pump_state = "on" if (farm2_should_turn_on and model_prediction == "on") else "off"
            else:  # previous state was "on"
                farm2_should_stay_on = farm2_moisture < (upper_threshold + buffer_zone)
                model_prediction = predict_pump_state(farm2_moisture)
                farm2_pump_state = "on" if (farm2_should_stay_on and model_prediction == "on") else "off"

            # Update previous states
            prev_farm1_state = farm1_pump_state
            prev_farm2_state = farm2_pump_state
            
            farm1_data = {
                "sender": "farm1",
                "moisture": farm1_moisture,
                "flow_meter": v_meter_2
            }
            
            farm2_data = {
                "sender": "farm2",
                "moisture": farm2_moisture,
                "flow_meter": v_meter_3
            }

            output = format_output(timestamp, farm1_data, farm1_pump_state, farm2_data, farm2_pump_state)
            print(json.dumps(output))
            
            time.sleep(10)

    except KeyboardInterrupt:
        running = False
        print("System stopped by user.")

    print("Program terminated.")
else:
    print(json.dumps({"error": "No input provided"}))