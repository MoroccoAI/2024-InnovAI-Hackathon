import sys
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime
from collections import deque

running = True

def load_and_split_data(csv_file):
    df = pd.read_csv(csv_file)
    df.drop(['Temperature', 'Air Humidity'], axis=1, inplace=True)
    
    # Split by pump state first
    on_data = df[df['Pump Data'] == 'on']
    off_data = df[df['Pump Data'] == 'off']
    
    # Balance the datasets
    min_size = min(len(on_data), len(off_data))
    balanced_on = on_data.sample(n=min_size, random_state=42)
    balanced_off = off_data.sample(n=min_size, random_state=42)
    
    # Combine and shuffle
    balanced_df = pd.concat([balanced_on, balanced_off]).sample(frac=1, random_state=42)
    
    # Split for two farms
    mid_point = len(balanced_df) // 2
    farm1_data = balanced_df.iloc[:mid_point]
    farm2_data = balanced_df.iloc[mid_point:]
    
    states_farm1 = list(zip(farm1_data['Soil Moisture'], farm1_data['Pump Data']))
    states_farm2 = list(zip(farm2_data['Soil Moisture'], farm2_data['Pump Data']))
    
    return create_q_tables(states_farm1, states_farm2)

def create_q_tables(states_farm1, states_farm2):
   num_moisture_buckets = 10
   num_pump_states = 2
   
   q_table_shape = (num_moisture_buckets, num_pump_states, 2)
   q_tables = {
       'farm1': np.zeros(q_table_shape),
       'farm2': np.zeros(q_table_shape)
   } 
   
   return q_tables

class QLearningIrrigation:
   def __init__(self, csv_file, learning_rate=0.1, discount_factor=0.95):
       self.q_tables = load_and_split_data(csv_file)
       self.lr = learning_rate
       self.gamma = discount_factor
       
   def get_state_index(self, moisture, prev_state):
       moisture_bucket = min(int(moisture / 10), 9)  # Ensure index doesn't exceed 9
       prev_state_index = 1 if prev_state == "on" else 0
       return (moisture_bucket, prev_state_index)
   
   def calculate_reward(self, moisture, action):
       reward = 0
       if 30 <= moisture <= 90:
           reward += 1
       elif moisture < 20 or moisture > 95:
           reward -= 2
       if action == "on":
           reward -= 0.1
       return reward
   
   def predict_action(self, farm, moisture, prev_state):
       state = self.get_state_index(moisture, prev_state)
       action_values = self.q_tables[farm][state]
       return "on" if np.argmax(action_values) == 1 else "off"
   
   def update(self, farm, state, action, reward, next_state):
       current_state = self.get_state_index(*state)
       next_state = self.get_state_index(*next_state)
       action_idx = 1 if action == "on" else 0
       
       old_value = self.q_tables[farm][current_state][action_idx]
       next_max = np.max(self.q_tables[farm][next_state])
       new_value = (1 - self.lr) * old_value + self.lr * (reward + self.gamma * next_max)
       self.q_tables[farm][current_state][action_idx] = new_value

class SensorBuffer:
   def __init__(self, size=5):
       self.buffer = deque(maxlen=size)
       
   def add_reading(self, value):
       self.buffer.append(value)
       
   def get_average(self):
       if not self.buffer:
           return 0
       return sum(self.buffer) / len(self.buffer)

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

   farm1_buffer = SensorBuffer()
   farm2_buffer = SensorBuffer()
   
   # Initialize Q-learning agent with CSV data
   q_agent = QLearningIrrigation('mapped_soil_data.csv')

   prev_farm1_state = "off"
   prev_farm2_state = "off"

   try:
       while running:
           timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
           
           farm1_buffer.add_reading(h1)
           farm2_buffer.add_reading(h3)
           
           farm1_moisture = farm1_buffer.get_average()
           farm2_moisture = farm2_buffer.get_average()
           
           # Farm 1 Q-learning control
           farm1_pump_state = q_agent.predict_action('farm1', farm1_moisture, prev_farm1_state)
           reward1 = q_agent.calculate_reward(farm1_moisture, farm1_pump_state)
           q_agent.update('farm1', 
                        (farm1_moisture, prev_farm1_state),
                        farm1_pump_state,
                        reward1,
                        (farm1_moisture, farm1_pump_state))

           # Farm 2 Q-learning control
           farm2_pump_state = q_agent.predict_action('farm2', farm2_moisture, prev_farm2_state)
           reward2 = q_agent.calculate_reward(farm2_moisture, farm2_pump_state)
           q_agent.update('farm2', 
                        (farm2_moisture, prev_farm2_state),
                        farm2_pump_state,
                        reward2,
                        (farm2_moisture, farm2_pump_state))

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
       # Save final Q-tables
       np.save('final_q_table_farm1.npy', q_agent.q_tables['farm1'])
       np.save('final_q_table_farm2.npy', q_agent.q_tables['farm2'])
       running = False
       print("System stopped by user.")

   print("Program terminated.")
else:
   print(json.dumps({"error": "No input provided"}))