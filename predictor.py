import pickle
import pandas as pd
from geopy.distance import geodesic
import ee
from google.oauth2 import service_account
import logging
import os
import gdown
import zipfile
import argparse

class WellNetworkPredictor:
    """
    Class to predict depth to water for new well locations based on well network and geospatial data.
    
    Attributes:
        rf_model: The pre-trained Random Forest model used for prediction.
        well_net: The well network graph containing existing well data.
    """
    
    def __init__(self, rf_model_filepath='bins/rf_depth_to_water.pkl', well_network_filepath='bins/well_network.gpickle', project='morocco-ai-2024'):
        """
        Initialize the WellNetworkPredictor class with a Random Forest model and well network graph.
        
        Args:
            rf_model_filepath (str): Path to the pre-trained Random Forest model.
            well_network_filepath (str): Path to the well network file.
            project (str): Earth Engine project name.
        """
        # Configure logging
        if not os.path.exists('log'):
            os.makedirs('log')
        logging.basicConfig(filename='log/predictor.log', level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(message)s')
        
        try:
            # Authenticate and initialize Google Earth Engine
            key_path = 'morocco-ai-2024-a2fad45fa0f6.json'
            credentials = service_account.Credentials.from_service_account_file(
                key_path, scopes=['https://www.googleapis.com/auth/earthengine']
            )
            logging.info("\nInitializing Google Earth Engine")
            ee.Initialize(credentials=credentials, project=project)
            logging.info("Google Earth Engine initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing Google Earth Engine: {e}")
        
        try:
            # Load the model and well network
            self.rf_model = self.load_rf_model(rf_model_filepath)
            self.well_net = self.load_well_network(well_network_filepath)
        except Exception as e:
            logging.error(f"Error loading model or well network: {e}")
            
    def download_and_extract_zip(self, zip_url, extract_to='bins'):
        try:
            zip_filepath = os.path.join(extract_to, 'model_and_network.zip')
            if not os.path.exists(zip_filepath):
                logging.info(f"{zip_filepath} not found. Downloading from {zip_url}.")
                gdown.download(zip_url, zip_filepath, quiet=False)
                logging.info(f"Downloaded ZIP file to: {zip_filepath}")
            else:
                logging.info(f"ZIP file already exists at: {zip_filepath}")
            
            if not os.path.exists(extract_to):
                os.makedirs(extract_to)
            
            logging.info(f"Extracting ZIP file to: {extract_to}")
            with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            logging.info("ZIP file extracted successfully")
        except Exception as e:
            logging.error(f"Error downloading or extracting ZIP file: {e}")
        
    def load_rf_model(self, filepath):
        try:
            if not os.path.exists(filepath):
                logging.info(f"{filepath} not found. Attempting to download and extract ZIP file.")
                zip_url = 'https://link.storjshare.io/s/jwrsgkkankl7zkpqjpwv3ahspoyq/moroccoai/model_and_network.zip?download=1'
                self.download_and_extract_zip(zip_url)
            
            logging.info(f"Loading Random Forest model from: {filepath}")
            with open(filepath, 'rb') as f:
                rf_model = pickle.load(f)
            logging.info("Random Forest model loaded successfully")
            return rf_model
        except Exception as e:
            logging.error(f"Error loading Random Forest model: {e}")
            return None

    def load_well_network(self, filepath):
        try:
            if not os.path.exists(filepath):
                logging.info(f"{filepath} not found. Attempting to download and extract ZIP file.")
                zip_url = 'https://link.storjshare.io/s/jwrsgkkankl7zkpqjpwv3ahspoyq/moroccoai/model_and_network.zip?download=1'
                self.download_and_extract_zip(zip_url)
            logging.info(f"Loading well network from: {filepath}")
            with open(filepath, 'rb') as f:
                well_net = pickle.load(f)
            logging.info("Well network loaded successfully")
            return well_net
        except Exception as e:
            logging.error(f"Error loading well network: {e}")
            return None
    
    def create_well_point(self, well_coordinates):
        try:
            return ee.Geometry.Point([well_coordinates[1], well_coordinates[0]])
        except Exception as e:
            logging.error(f"Error creating well point: {e}")
            return None

    def fetch_climate_data(self, start_date, end_date, well_point):
        try:
            climate_data = ee.ImageCollection("OREGONSTATE/PRISM/AN81m") \
                .filterDate(start_date, end_date) \
                .select(['tmean', 'ppt'])
            climate_clip = climate_data.mean().clip(well_point.buffer(1000))
            climate_stats = climate_clip.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=well_point,
                scale=1000
            )
            return climate_stats
        except Exception as e:
            logging.error(f"Error fetching climate data: {e}")
            return None
    
    def fetch_soil_data(self, well_point):
        try:
            soil_data = {}
            soil_types = {
                "ph": "OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02",
                "carbon": "OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02",
                "sand": "OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02",
                "silt": "OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02",
                "clay": "OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02"
            }
            
            for soil_type, image_id in soil_types.items():
                soil_data[soil_type] = self.fetch_single_soil_stat(image_id, well_point)
            
            return soil_data
        except Exception as e:
            logging.error(f"Error fetching soil data: {e}")
            return None
    
    def fetch_single_soil_stat(self, image_id, well_point):
        try:
            soil_data = ee.Image(image_id)
            soil_clip = soil_data.clip(well_point.buffer(30))
            soil_stats = soil_clip.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=well_point,
                scale=30
            )
            return soil_stats
        except Exception as e:
            logging.error(f"Error fetching single soil stat: {e}")
            return None

    def get_soil_climate_data(self, well_coordinates, start_date = '2023-01-01', end_date =  '2023-12-31'):
        try:
            well_point = self.create_well_point(well_coordinates)
            
            logging.info(f"Fetching soil and climate data for location: {well_coordinates}")
            climate_stats = self.fetch_climate_data(start_date, end_date, well_point)
            logging.info(f"Climate data fetched successfully")
            logging.info(f"Climate data: {climate_stats.getInfo()}")
            soil_data = self.fetch_soil_data(well_point)
            logging.info(f"Soil data fetched successfully")
            
            combined_data = {
                "soil_ph": soil_data["ph"].getInfo(),
                "soil_carbon": soil_data["carbon"].getInfo(),
                "soil_sand": soil_data["sand"].getInfo(),
                "soil_silt": soil_data["silt"].getInfo(),
                "soil_clay": soil_data["clay"].getInfo(),
                "climate_conditions": climate_stats.getInfo(),
            }
            return combined_data
        except Exception as e:
            logging.error(f"Error getting soil and climate data: {e}")
            return None

    def json_to_dataframe(self, json_data):
        try:
            data = {}
            for key in json_data.keys():
                if isinstance(json_data[key], dict):
                    sub_data = self.json_to_dataframe(json_data[key])
                    for sub_key in sub_data.keys():
                        data[f"{key}_{sub_key}"] = sub_data[sub_key]
                else:
                    data[key] = json_data[key]
            return data
        except Exception as e:
            logging.error(f"Error converting JSON to DataFrame: {e}")
            return None
    
    def add_new_node_and_edges(self, new_location_coords, threshold_km=5):
        try:
            new_lat, new_lon = new_location_coords
            logging.info(f"Adding new node at location: {new_location_coords}")
            self.well_net.add_node('new_node')
            logging.info(f"New node added successfully")
            
            logging.info(f"Adding edges to neighbors within {threshold_km} km")
            for i in self.well_net.nodes:
                if i != 'new_node':
                    existing_lat = self.well_net.nodes[i]['Lat']
                    existing_lon = self.well_net.nodes[i]['Lon']
                    distance = geodesic((new_lat, new_lon), (existing_lat, existing_lon)).kilometers
                    if distance < threshold_km:
                        self.well_net.add_edge('new_node', i, weight=distance)
            logging.info(f"Edges added successfully")
        except Exception as e:
            logging.error(f"Error adding new node and edges: {e}")
    
    def remove_new_node(self):
        try:
            self.well_net.remove_node('new_node')
            logging.info("New node removed successfully")
        except Exception as e:
            logging.error(f"Error removing new node: {e}")
    
    def compute_depth_using_neighbors(self):
        try:
            total_weight = 0
            weighted_sum = 0
            
            logging.info("Computing depth using neighbors")        
            for neighbor in self.well_net.neighbors('new_node'):
                weight = 1 / self.well_net.edges['new_node', neighbor]['weight'] if self.well_net.edges['new_node', neighbor]['weight'] > 0 else 0
                weighted_sum += self.well_net.nodes[neighbor]['DepthToWater_m'] * weight
                total_weight += weight
            
            if total_weight > 0:
                logging.info(f"Computed depth using neighbors: {weighted_sum / total_weight} meters")
                return weighted_sum / total_weight
            logging.warning("No neighbors found within threshold distance")
            return None
        except Exception as e:
            logging.error(f"Error computing depth using neighbors: {e}")
            return None

    def predict_depth_with_rf_model(self, new_location_coords):
        try:
            extra_data = self.get_soil_climate_data(new_location_coords)
            extra_data_flat = self.json_to_dataframe(extra_data)
            
            combined_features = {
                'Lat': new_location_coords[0],
                'Lon': new_location_coords[1],
            }
            combined_features.update(extra_data_flat)
            
            features = [
                "soil_ph_b0", "soil_ph_b10", "soil_ph_b100", "soil_ph_b200", "soil_ph_b30", "soil_ph_b60", 
                "soil_carbon_b0", "soil_carbon_b10", "soil_carbon_b100", "soil_carbon_b200", "soil_carbon_b30", "soil_carbon_b60", 
                "soil_sand_b0", "soil_sand_b10", "soil_sand_b100", "soil_sand_b200", "soil_sand_b30", "soil_sand_b60", 
                "soil_silt_b0", "soil_silt_b10", "soil_silt_b100", "soil_silt_b200", "soil_silt_b30", "soil_silt_b60", 
                "soil_clay_b0", "soil_clay_b10", "soil_clay_b100", "soil_clay_b200", "soil_clay_b30", "soil_clay_b60", 
                "climate_conditions_ppt", "climate_conditions_tmean", "Lat", "Lon"
            ]
            
            combined_features_vector = pd.DataFrame([list(combined_features.values())], columns=features)
            
            return self.rf_model.predict(combined_features_vector)[0]
        except Exception as e:
            logging.error(f"Error predicting depth with Random Forest model: {e}")
            return None
    
    def compute_and_predict_depth_of_water(self, new_location_coords, threshold_km=5):
        # shift to fit Morocco's coordinates inside USA's bounding box since the model was trained on USA data
        # ONLY FOR TESTING PURPOSES
        new_location_coords = list(new_location_coords)
        new_location_coords[0] += 2.5
        new_location_coords[1] -= 80.0
        try:
            logging.info(f"Starting prediction for location: {new_location_coords} with threshold: {threshold_km} km")
            
            self.add_new_node_and_edges(new_location_coords, threshold_km)
            
            predicted_depth = None
            if self.well_net.degree('new_node') > 0:
                predicted_depth = self.compute_depth_using_neighbors()
                logging.info(f"Predicted depth using neighbors: {predicted_depth} meters")
            else:
                predicted_depth = self.predict_depth_with_rf_model(new_location_coords)
                logging.info(f"Predicted depth using Random Forest model: {predicted_depth} meters")
            
            self.remove_new_node()
            logging.info(f"Prediction completed for location: {new_location_coords}")
            return predicted_depth
        except Exception as e:
            logging.error(f"Error computing and predicting depth of water: {e}")
            return None

parser = argparse.ArgumentParser(description ='Take some input')
parser.add_argument("--lon", type=float, required=True, help="Longitude value")
parser.add_argument("--lat", type=float, required=True, help="Latitude value")
args = parser.parse_args()
    
lon = args.lon
lat = args.lat
predictplz = WellNetworkPredictor()
new_location_coords = (lat, lon)
predicted_depth = predictplz.compute_and_predict_depth_of_water(new_location_coords)
print(predicted_depth)

# # location in USA
# python predictor.py --lon -122.3321 --lat 47.6062