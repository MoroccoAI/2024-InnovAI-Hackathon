# Reducing the Impact of Agriculture on Drought by Optimizing Water Use Using Machine Learning AMANE 🌾💧

## Abstract

### Background and Problem Statement
Water scarcity, aggravated by recurrent droughts, presents a significant challenge to sustainable agricultural practices in Morocco. The country's "Maroc-Vert" strategy emphasizes boosting agricultural productivity for economic growth. However, this initiative places immense pressure on already limited water resources. Traditional irrigation methods are inefficient, as they fail to consider dynamic factors such as soil moisture, weather conditions, and crop needs. Consequently, there is an urgent need for an innovative solution that optimizes water usage, ensures food security, and supports sustainable agriculture.

### Impact and Proposed Solution
This project leverages machine learning (ML) to enhance irrigation efficiency and optimize water resource management. By processing real-time data on environmental conditions, soil moisture, and weather patterns, the proposed ML models will predict irrigation needs, identify drought-resistant crops, and distribute water resources more effectively. This solution promises to:
- 🌱 Conserve water resources by minimizing waste.
- 🌾 Improve crop yields through precise water allocation.
- 🌍 Support economic growth and environmental sustainability.
- ⚠ Provide early warning systems for drought conditions to prevent crises.

### Project Outcomes and Deliverables
The primary outcomes and deliverables of this project include:
1. **Irrigation Optimization Model**: Predicts optimal irrigation timing and amounts.
2. **Water Resource Allocation Tool**: Ensures effective distribution of water among competing needs.
3. **Drought Prediction System**: Provides early warnings to mitigate risks.
4. **User-Friendly Application**: A mobile/web application for farmers and policymakers to access insights and recommendations.

### Features
- 📊 **Dashboard**: Visualize irrigation recommendations, water usage statistics, and crop suggestions.
- 🌦 **Drought Prediction**: Alerts displayed based on real-time weather data.

---

## Deployment and API Documentation

### Model Deployment
The irrigation prediction model has been deployed on **Azure** and is ready for real-world use.  
**Endpoint**: [https://recommendationmodel-cfb9fycaguhpegbs.spaincentral-01.azurewebsites.net/](https://recommendationmodel-cfb9fycaguhpegbs.spaincentral-01.azurewebsites.net/)

### Predict Irrigation API

**Endpoint**:  
`POST /predict_irrigation`

**Description**:  
Provides real-time irrigation recommendations based on environmental and soil data.

**Expected Input**:  
A JSON payload with the following features:
```json
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
```

| Feature Name              | Description                             | Example Value |
|---------------------------|-----------------------------------------|---------------|
| `electrical_conductivity` | Soil electrical conductivity (dS/m)    | 0.7           |
| `soil_moisture`           | Soil moisture content (%)              | 25.3          |
| `soil_temperature`        | Soil temperature (°C)                  | 18.5          |
| `env_humidity`            | Environmental humidity (%)             | 60.2          |
| `env_temperature`         | Environmental temperature (°C)         | 23.4          |
| `precipitations_mm`       | Precipitation levels (mm)              | 2.0           |
| `humidity`                | Overall humidity levels (%)            | 65.0          |
| `et0_fao`                 | Evapotranspiration (FAO Penman-Monteith) | 5.5          |

**Example Request**:
```bash
curl -X POST https://recommendationmodel-cfb9fycaguhpegbs.spaincentral-01.azurewebsites.net/predict_irrigation \
-H "Content-Type: application/json" \
-d '{
    "features": [0.7, 25.3, 18.5, 60.2, 23.4, 2.0, 65.0, 5.5]
}'
```

**Example Response**:
```json
{
    "prediction": "ON",
    "message": "Irrigation prediction successful"
}
```

**Error Handling**:
- If the request payload is missing or invalid:
```json
{
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
}
```

- If an internal error occurs:
```json
{
    "error": "An error occurred during prediction",
    "details": "Specific error message"
}
```

---

### How to Make Our App Work 🚀
To run the application locally, follow these steps:
1. Clone the repository to your local machine.
2. Navigate to the project folder and run `npm install` to install the necessary dependencies.
3. Start the server with `npm start`.
4. Access the app at `http://localhost:3000`. **Note: Make sure to use `localhost:3000` for local testing**.

We used **Azure & Github Actions** for deploying all the API endpoints in the code, ensuring scalability and reliability for real-world use.
