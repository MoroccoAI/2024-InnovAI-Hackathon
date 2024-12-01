import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Define the API endpoint
api_url = "https://8791-34-40-149-146.ngrok-free.app/predict"

payload = {
    "days_to_predict": 7  # Predict the next 7 days
}

try:
    # Send a POST request to the API
    response = requests.post(api_url, json=payload)
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.json()

    # Extract predictions and timestamps from the response
    predictions = data["predictions"]
    timestamps = data["timestamps"]

    # Convert timestamps to datetime objects
    timestamps = [datetime.strptime(ts, "%Y-%m-%d") for ts in timestamps]

    # Plot the predictions
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, predictions, marker="o", label="Predicted Meter Reading", color="orange")
    plt.title("Forecasted Meter Reading")
    plt.xlabel("Date")
    plt.ylabel("Meter Reading")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching predictions: {e}")
