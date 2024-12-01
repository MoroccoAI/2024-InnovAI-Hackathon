from flask import Flask, request, jsonify,Response
import threading
import joblib
import pandas as pd
import json
import numpy as np
from flask_cors import CORS 
import os
from azure.storage.blob import BlobServiceClient
import time
from datetime import datetime
from collections import deque
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")


if not AZURE_STORAGE_CONNECTION_STRING or not CONTAINER_NAME:
    raise ValueError("Azure Storage connection string or container name not set in environment variables.")


blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def download_blob(blob_name, download_path):
    try:
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
    except Exception as e:
        print(f"Failed to download blob {blob_name}: {e}")
        raise


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

artifacts_dir = os.path.join(BASE_DIR, 'artifacts')
if not os.path.exists(artifacts_dir):
    os.makedirs(artifacts_dir)
    
movie_list_path = os.path.join(BASE_DIR, 'artifacts', 'movie_list.joblib')
similarity_matrix_path = os.path.join(BASE_DIR, 'artifacts', 'similarity.joblib')
best_gbr_path= os.path.join(BASE_DIR, 'artifacts', 'temperature_model.joblib')
initial_sequenceT_path= os.path.join(BASE_DIR, 'artifacts', 'initial_sequenceT.joblib')
scaler_path=os.path.join(BASE_DIR, 'artifacts', 'scaler.joblib')
humidity_model_path = os.path.join(BASE_DIR, 'artifacts', 'humidity_model.joblib')
initial_sequenceH_path= os.path.join(BASE_DIR, 'artifacts', 'initial_sequenceH.joblib')
condec_model_path=os.path.join(BASE_DIR,'artifacts', 'condic_model.joblib')
initial_sequenceD_path= os.path.join(BASE_DIR, 'artifacts', 'initial_sequenceD.joblib')

env_co2_model_path=os.path.join(BASE_DIR,'artifacts','co2_model.joblib')
env_initial_sequenceCO2_path=os.path.join(BASE_DIR,'artifacts','initial_sequenceCO2.joblib')
env_tempra_model_path=os.path.join(BASE_DIR,'artifacts','env_temperature_model.joblib')
env_temperature_initial_sequence_path=os.path.join(BASE_DIR,'artifacts','env_temperature_initial_sequence.joblib')
env_humidity_model_path = os.path.join(BASE_DIR, 'artifacts', 'env_humidity_model.joblib')
env_humidity_initial_sequence_path= os.path.join(BASE_DIR, 'artifacts', 'env_humidity_initial_sequence.joblib')
ann_model_path=os.path.join(BASE_DIR,'artifacts','ann_model.joblib')
StandardScaler_path=os.path.join(BASE_DIR,'artifacts','StandardScaler.joblib')
label_encoder_path=os.path.join(BASE_DIR,'artifacts','label_encoder.joblib')

if not os.path.exists(label_encoder_path):
    download_blob('label_encoder.joblib',label_encoder_path)

if not os.path.exists(ann_model_path):
    download_blob('ann_model.joblib',ann_model_path)
if not os.path.exists(StandardScaler_path):
    download_blob('StandardScaler.joblib',StandardScaler_path)
if not os.path.exists(env_humidity_model_path):
    download_blob('env_humidity_model.joblib',env_humidity_model_path)

if not os.path.exists(env_humidity_initial_sequence_path):
    download_blob('env_humidity_initial_sequence.joblib',env_humidity_initial_sequence_path)

if not os.path.exists(env_tempra_model_path):
    download_blob('env_temperature_model.joblib',env_tempra_model_path)

if not os.path.exists(env_temperature_initial_sequence_path):
    download_blob('env_temperature_initial_sequence.joblib',env_temperature_initial_sequence_path)

if not os.path.exists(env_co2_model_path):
    download_blob('co2_model.joblib',env_co2_model_path)

if not os.path.exists(env_initial_sequenceCO2_path):
    download_blob('initial_sequenceCO2.joblib',env_initial_sequenceCO2_path)


if not os.path.exists(condec_model_path):
    download_blob('condic_model.joblib',condec_model_path)
if not os.path.exists(initial_sequenceD_path):
    download_blob('initial_sequenceD.joblib',initial_sequenceD_path)

if not os.path.exists(best_gbr_path):
    download_blob("temperature_model.joblib", best_gbr_path)

if not os.path.exists(initial_sequenceT_path):
    download_blob("initial_sequenceT.joblib", initial_sequenceT_path)

if not os.path.exists(scaler_path):
    download_blob("scaler.joblib",scaler_path)


if not os.path.exists(movie_list_path):
    download_blob("movie_list.joblib", movie_list_path)

if not os.path.exists(similarity_matrix_path):
    download_blob("similarity.joblib", similarity_matrix_path)

if not os.path.exists(humidity_model_path):
    download_blob("humidity_model.joblib", humidity_model_path)
if not os.path.exists(initial_sequenceH_path):
    download_blob("initial_sequenceH.joblib",initial_sequenceH_path)
try:
    movies = joblib.load(movie_list_path)
    similarity_matrix = joblib.load(similarity_matrix_path)
    best_gbr = joblib.load(best_gbr_path)
    initial_sequenceT= joblib.load(initial_sequenceT_path)
    scaler=joblib.load(scaler_path)
    humidity_model = joblib.load(humidity_model_path)
    initial_sequenceH = joblib.load(initial_sequenceH_path)
    condic_model=joblib.load(condec_model_path)
    initial_sequenceD=joblib.load(initial_sequenceD_path)
    co2_model=joblib.load(env_co2_model_path)
    env_initial_sequenceCO2=joblib.load(env_initial_sequenceCO2_path)
    env_tempra_model=joblib.load(env_tempra_model_path)
    env_temperature_initial_sequence=joblib.load(env_temperature_initial_sequence_path)
    env_humidity_initial_sequence=joblib.load(env_humidity_initial_sequence_path)
    env_humidity_model=joblib.load(env_humidity_model_path)
    ann_model=joblib.load(ann_model_path)
    StandardScaler=joblib.load(StandardScaler_path)
    label_encoder=joblib.load(label_encoder_path)

except Exception as e:
    print(f"Error loading model files: {e}")
    raise

MAX_BUFFER_SIZE = 100
simulated_data = {
    "temperature": deque(maxlen=MAX_BUFFER_SIZE),
    "humidity": deque(maxlen=MAX_BUFFER_SIZE),
    "conductivity": deque(maxlen=MAX_BUFFER_SIZE),
    "env_co2": deque(maxlen=MAX_BUFFER_SIZE),
    "env_temperature": deque(maxlen=MAX_BUFFER_SIZE),
    "env_humidity": deque(maxlen=MAX_BUFFER_SIZE)
}
data_lock = threading.Lock()


def simulate_co2_sensor(model, initial_sequence, scaler, interval=1, steps=100):
    """
    Simulates CO2 sensor with realistic seasonal variations.
    
    Parameters:
    - model: Trained machine learning model for prediction
    - initial_sequence: Initial sequence of CO2 readings
    - scaler: Scaler used for normalizing/denormalizing data
    - interval: Base time interval between measurements
    - steps: Number of simulation steps
    
    Returns:
    - List of simulated CO2 measurements
    """
    sequence = np.array(initial_sequence)
    # Baseline CO2 level (global average)
    baseline_co2 = 419.3  # ppm in 2023

    for step in range(steps):
        # Predict next CO2 value using model
        next_scaled_value = model.predict(sequence.reshape(1, -1))
        next_co2 = scaler.inverse_transform(next_scaled_value.reshape(-1, 1))[0, 0]

        # Get current date to calculate seasonal variation
        current_date = datetime.now()
        day_of_year = current_date.timetuple().tm_yday

        # Seasonal variation simulation
        # Peak CO2 in late winter/early spring, lowest in late summer
        seasonal_amplitude = 10  # Maximum variation of 10 ppm
        seasonal_offset = seasonal_amplitude * np.sin(
            2 * np.pi * (day_of_year - 80) / 365  # Shifted to align with natural cycle
        )

        # Combine baseline, model prediction, and seasonal variation
        next_co2 = baseline_co2 + next_co2 + seasonal_offset

        # Long-term trend (global CO2 increase)
        annual_increase_rate = 2.5  # ppm per year
        trend_adjustment = (annual_increase_rate / 365) * step

        next_co2 += trend_adjustment

        # Constrain CO2 values to realistic range
        next_co2 = max(min(next_co2, 500), 400)
        with data_lock:
            simulated_data["env_co2"].append(next_co2)

        # Update sequence for next prediction
        sequence = np.roll(sequence, -1)
        sequence[-1] = next_scaled_value[0]
 
        time.sleep(interval)

    

def simulate_env_temperature_sensor(model, initial_sequence, scaler, interval=1, steps=100):
    """
    Simulates a real-time temperature sensor using a trained model with added realism.
    """

    sequence = np.array(initial_sequence)

    for _ in range(steps):
        next_scaled_value = model.predict(sequence.reshape(1, -1))
        next_temperature = scaler.inverse_transform(next_scaled_value.reshape(-1, 1))[0, 0]
        noise = np.random.normal(0, 0.5)
        next_temperature += noise
    
        seasonal_pattern = np.sin(time.time() / 86400 * 2 * np.pi) * 2  
        next_temperature += seasonal_pattern

      
        drift = 0.01  
        next_temperature += drift

        next_temperature = max(min(next_temperature, 40), -10) 

      
        if np.random.rand() < 0.1:
            next_temperature += np.random.choice([-5, 5])

        with data_lock:
           simulated_data["env_temperature"].append(next_temperature)
        sequence = np.roll(sequence, -1) 
        sequence[-1] = next_scaled_value[0] 

        
        time.sleep(interval)
def simulate_environmental_humidity_sensor(model, initial_sequence, scaler, interval=1, steps=100):
    """
    Simulates environmental humidity with variations typical of Morocco's climate.
    
    Parameters:
    - model: Trained machine learning model for prediction
    - initial_sequence: Initial sequence of humidity readings
    - scaler: Scaler used for normalizing/denormalizing data
    - interval: Base time interval between measurements
    - steps: Number of simulation steps
    
    Returns:
    - List of simulated humidity measurements
    """


    sequence = np.array(initial_sequence)
   

    for _ in range(steps):
        # Predict next humidity value using model
        next_scaled_value = model.predict(sequence.reshape(1, -1))
        next_humidity = scaler.inverse_transform(next_scaled_value.reshape(-1, 1))[0, 0]

        # Get current date to calculate seasonal variation
        current_date = datetime.now()
        day_of_year = current_date.timetuple().tm_yday

        # Seasonal variation simulation
        # Highest humidity in winter, lowest in summer
        seasonal_amplitude = 20  # More pronounced due to Morocco's climate
        seasonal_offset = seasonal_amplitude * np.sin(
            2 * np.pi * (day_of_year - 80) / 365  # Adjusted to peak in winter months
        )

        # Combine base humidity, model prediction, and seasonal variation
        next_humidity = (
            next_humidity + 
            seasonal_offset
        )

        # Slight drift to simulate long-term changes
        drift = 0.1
        next_humidity += drift

        # Constrain humidity to realistic range for Morocco
        # Humidity can range from very low in desert areas to higher in coastal regions
        next_humidity = max(min(next_humidity, 90), 20)

        # Occasional more significant fluctuations
        if np.random.rand() < 0.1:
            next_humidity += np.random.choice([-15, 15])
        with data_lock:
            simulated_data["env_humidity"].append(next_humidity)

        # Update sequence for next prediction
        sequence = np.roll(sequence, -1)
        sequence[-1] = next_scaled_value[0]

        # Time interval variation
        time.sleep(interval)


def simulate_temperature_sensor(model, initial_sequence, scaler, interval=1, steps=100):
    """
    Simulates a real-time temperature sensor using a trained model with added realism.
    """

    sequence = np.array(initial_sequence)

    for _ in range(steps):
        next_scaled_value = model.predict(sequence.reshape(1, -1))
        next_temperature = scaler.inverse_transform(next_scaled_value.reshape(-1, 1))[0, 0]
        noise = np.random.normal(0, 0.5)
        next_temperature += noise
    
        seasonal_pattern = np.sin(time.time() / 86400 * 2 * np.pi) * 2  
        next_temperature += seasonal_pattern

      
        drift = 0.01  
        next_temperature += drift

        next_temperature = max(min(next_temperature, 40), -10) 

      
        if np.random.rand() < 0.1:
            next_temperature += np.random.choice([-5, 5])

        with data_lock:
            simulated_data["temperature"].append(next_temperature)
        sequence = np.roll(sequence, -1) 
        sequence[-1] = next_scaled_value[0] 

        
        time.sleep(interval)

def simulate_soil_humidity_sensor(model, initial_sequence, scaler, interval=1, steps=100):
    sequence = np.array(initial_sequence)

    for _ in range(steps):
        next_scaled_value = model.predict(sequence.reshape(1, -1))
        next_humidity = scaler.inverse_transform(next_scaled_value.reshape(-1, 1))[0, 0]

        noise = np.random.normal(0, 1)
        next_humidity += noise

        seasonal_pattern = np.sin(time.time() / 86400 * 2 * np.pi) * 1.5
        next_humidity += seasonal_pattern

        drift = 0.005
        next_humidity += drift

        next_humidity = max(min(next_humidity, 100), 0)

        if np.random.rand() < 0.1:
            next_humidity += np.random.choice([-10, 10])

        with data_lock:
            simulated_data["humidity"].append(next_humidity)

        sequence = np.roll(sequence, -1)
        sequence[-1] = next_scaled_value[0]

        time.sleep(interval)

def simulate_electrical_conductivity_sensor(model, initial_sequence, scaler, interval=1, steps=100):
    """
    Simulates a real-time electrical conductivity sensor using a trained model with added realism.
    
    :param model: Trained GradientBoostingRegressor model
    :param initial_sequence: The starting sequence (last known electrical conductivity values)
    :param scaler: The scaler used for normalization
    :param interval: Time interval between sensor readings in seconds (default: 3 seconds)
    :param steps: Number of steps to simulate (default: 100)
    
    :return: None
    """
    sequence = np.array(initial_sequence)

    for _ in range(steps):
        # Predict the next value (scaled)
        next_scaled_value = model.predict(sequence.reshape(1, -1))
        
        # Inverse transform to get the predicted conductivity value
        next_conductivity = scaler.inverse_transform(next_scaled_value.reshape(-1, 1))[0, 0]
        
        # Add Gaussian noise to simulate sensor imperfections (mean=0, std=0.01)
        noise = np.random.normal(0, 0.01)
        next_conductivity += noise
        
        # Simulate seasonal fluctuations (small amplitude sine wave)
        seasonal_pattern = np.sin(time.time() / 86400 * 2 * np.pi) * 0.1  # Adding a small seasonal fluctuation
        next_conductivity += seasonal_pattern
        
        # Simulate drift (slow gradual change in conductivity)
        drift = 0.001  # Slight drift over time
        next_conductivity += drift
        
        # Enforce realistic conductivity range (0 to 10 S/m)
        next_conductivity = max(min(next_conductivity, 10), 0)
        
        # Occasionally introduce sudden changes (e.g., due to irrigation or environmental events)
        if np.random.rand() < 0.1:  # 10% chance of a sudden change
            next_conductivity += np.random.choice([-0.5, 0.5])  # Sudden change in conductivity
        
        # Store the simulated conductivity value
        with data_lock:
            simulated_data["conductivity"].append(next_conductivity)
        
        # Update the sequence with the new prediction (shift and append)
        sequence = np.roll(sequence, -1)
        sequence[-1] = next_scaled_value[0]
        
        # Vary the interval slightly for more realism (±10%)
        time.sleep(interval)

def run_simulation():
    simulate_temperature_sensor(best_gbr, initial_sequenceT, scaler)

def run_humidity_simulation():
    simulate_soil_humidity_sensor(humidity_model, initial_sequenceH, scaler)

def run_condective_simulation():
    simulate_electrical_conductivity_sensor(condic_model, initial_sequenceD, scaler)

def run_env_co2_simulation():
    simulate_co2_sensor(co2_model, env_initial_sequenceCO2, scaler)

def run_env_temperature_simulation():
    simulate_env_temperature_sensor(env_tempra_model, env_temperature_initial_sequence, scaler)

def run_env_humidity_simulation():
    simulate_environmental_humidity_sensor(env_humidity_model, env_humidity_initial_sequence, scaler)


simulation_threads = {
    "temperature": None,
    "humidity": None,
    "conductivity": None,
    "env_co2": None,
    "env_temperature": None,
    "env_humidity": None
}


# Enhanced streaming mechanism
def generate_data(sensor_type):
    while True:
        with data_lock:
            if simulated_data.get(sensor_type):
                data = {sensor_type: simulated_data[sensor_type][-1]}
                yield f"data: {json.dumps(data)}\n\n"
            else:
                yield f"data: {json.dumps({})}\n\n"
        time.sleep(0.5)  # Reduced sleep time for faster streaming

#model, 
def prepare_single_row_for_prediction(features_array, model, scaler,label_encoder):
    sample_row = np.array(features_array)

    # Scaling features
    sample_row_scaled = scaler.transform(sample_row.reshape(1, -1))

    # Predict using the ANN model
    prediction = model.predict(sample_row_scaled)

    # Get the predicted class index
    predicted_class_index = np.argmax(prediction)

    # Decode the predicted class using the label encoder
    predicted_class = label_encoder.inverse_transform([predicted_class_index])
    
    return predicted_class[0]



@app.route('/')
def home():
    return "Welcome to the Movie Sensores API!"

@app.route('/predict_irrigation', methods=['POST'])
def predict_irrigation():
    """
    Real-time prediction route for irrigation recommendation.
    
    Expects a JSON payload with feature values:
    {
        "features": [
            electrical_conductivity, 
            soil_moisture, 
            soil_temperature, 
            env_humidity, 
            env_temperature, 
            precipitations_mm, 
            humidity, 
            et0_fao
        ]
    }
    
    Returns the predicted irrigation recommendation.
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if 'features' not in data or len(data['features']) != 8:
            return jsonify({
                "error": "Invalid input. Exactly 8 feature values are required.",
                "expected_features": [
                    "electrical_conductivity", 
                    "soil_moisture", 
                    "soil_temperature", 
                    "env_humidity", 
                    "env_temperature", 
                    "precipitations_mm", 
                    "humidity", 
                    "et0_fao"
                ]
            }), 400
        
        # Prepare features and make prediction
        prediction = prepare_single_row_for_prediction(
            data['features'], 
            ann_model,  # Using the conductivity model for prediction
            StandardScaler,
            label_encoder
        )
        
        return jsonify({
            "prediction": prediction,
            "message": "Irrigation prediction successful"
        })
    
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            "error": "An error occurred during prediction",
            "details": str(e)
        }), 500

@app.route('/start_temp_simulation', methods=['GET'])
def start_temperature_simulation():
    simulated_data["temperature"].clear()
    
    if simulation_threads["temperature"] is None or not simulation_threads["temperature"].is_alive():
        simulation_threads["temperature"] = threading.Thread(target=run_simulation)
        simulation_threads["temperature"].start()

    return Response(generate_data("temperature"), content_type='text/event-stream')


@app.route('/start_humidity_simulation', methods=['GET'])
def start_humidity_simulation():
    simulated_data["humidity"].clear()

    if simulation_threads["humidity"] is None or not simulation_threads["humidity"].is_alive():
        simulation_threads["humidity"] = threading.Thread(target=run_humidity_simulation)
        simulation_threads["humidity"].start()

    return Response(generate_data("humidity"), content_type='text/event-stream')


@app.route('/start_conductivity_simulation', methods=['GET'])
def start_conductivity_simulation():
    simulated_data["conductivity"].clear()

    if simulation_threads["conductivity"] is None or not simulation_threads["conductivity"].is_alive():
        simulation_threads["conductivity"] = threading.Thread(target=run_condective_simulation)
        simulation_threads["conductivity"].start()

    return Response(generate_data("conductivity"), content_type='text/event-stream')

@app.route('/start_env_co2_simulation', methods=['GET'])
def start_env_co2_simulation():
    simulated_data["env_co2"].clear()
    
    if simulation_threads["env_co2"] is None or not simulation_threads["env_co2"].is_alive():
        simulation_threads["env_co2"] = threading.Thread(target=run_env_co2_simulation)
        simulation_threads["env_co2"].start()

    return Response(generate_data("env_co2"), content_type='text/event-stream')

@app.route('/start_env_temperature_simulation', methods=['GET'])
def start_env_temperature_simulation():
    simulated_data["env_temperature"].clear()
    
    if simulation_threads["env_temperature"] is None or not simulation_threads["env_temperature"].is_alive():
        simulation_threads["env_temperature"] = threading.Thread(target=run_env_temperature_simulation)
        simulation_threads["env_temperature"].start()

    return Response(generate_data("env_temperature"), content_type='text/event-stream')

@app.route('/start_env_humidity_simulation', methods=['GET'])
def start_env_humidity_simulation():
    simulated_data["env_humidity"].clear()
    
    if simulation_threads["env_humidity"] is None or not simulation_threads["env_humidity"].is_alive():
        simulation_threads["env_humidity"] = threading.Thread(target=run_env_humidity_simulation)
        simulation_threads["env_humidity"].start()

    return Response(generate_data("env_humidity"), content_type='text/event-stream')

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    Recommends similar movies based on the provided movie title.
    
    Expects JSON input: {"title": "movie_name"}
    """
    data = request.get_json()
    movie_title = data.get('title')

    
    if not movie_title:
        return jsonify({"error": "Movie title not provided."}), 400
    

    try:
        
        movie_index = movies[movies['title'].str.lower() == movie_title.lower()].index[0]
        movie_index = int(movie_index)  # Convert the index to a native Python integer type
    except IndexError:
        return jsonify({"error": f"Movie '{movie_title}' not found in the dataset."}), 404
    except Exception as e:
        print(f"An unexpected error occurred while searching for the movie: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

    print(f"Movie Index: {movie_index} (Type: {type(movie_index)})")

    try:
       
        if not isinstance(similarity_matrix, np.ndarray) or similarity_matrix.shape[0] != similarity_matrix.shape[1]:
            return jsonify({"error": "Invalid similarity matrix shape. It must be square."}), 500

        
        similarity_scores = list(enumerate(similarity_matrix[movie_index]))
        print(f"Similarity Scores: {similarity_scores[:5]}")  # Print first 5 similarity scores for debugging


        sorted_similar_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:11]
        print(f"Sorted Similar Movies: {sorted_similar_movies}")


        recommended_titles = [movies.iloc[i[0]].title for i in sorted_similar_movies]

        return jsonify({"recommendations": recommended_titles})

    except Exception as e:
        print(f"An error occurred while processing the similarity matrix: {e}")
        return jsonify({"error": "An error occurred while processing the similarity matrix."}), 500



@app.route('/get_latest_sensor_data', methods=['GET'])
def get_latest_sensor_data():
    """
    Retrieves the latest data for all sensors in a single API call
    """
    latest_data = {}
    with data_lock:
        for sensor_type, data in simulated_data.items():
            if data:
                latest_data[sensor_type] = data[-1]
    
    return jsonify(latest_data)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, threaded=True)
