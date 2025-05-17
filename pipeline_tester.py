import requests
import torch
import torch.nn as nn
import numpy as np
from hybrid_fusion_pipeline import HybridFusionModel

# --- Constants ---
LATITUDE = 47.4979
LONGITUDE = 19.0402
HEALTH_FEATURES = 3  # dynamically handles number of health features

# --- Data Fetcher ---
def fetch_environmental_data(lat, lon):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"

    weather = requests.get(weather_url).json()["hourly"]
    air = requests.get(air_url).json()["hourly"]

    data_vector = [
        weather["temperature_2m"][0],
        weather["relative_humidity_2m"][0],
        weather["wind_speed_10m"][0],
        air["pm10"][0],
        air["pm2_5"][0],
        air["carbon_monoxide"][0],
        air["nitrogen_dioxide"][0],
        air["sulphur_dioxide"][0],
        air["ozone"][0]
    ]

    print("Fetched Environmental Data:", data_vector)
    return data_vector

# --- Main Entry ---
if __name__ == "__main__":
    # 1. Health data with 3 features: [Body Temp, Pulse, BP]
    vital_signs_data = [
        [36.7, 72, 118],
        [37.0, 76, 122],
        [36.8, 70, 115],
        [37.2, 80, 125],
        [36.9, 74, 119],
        [37.1, 78, 121],
        [36.6, 68, 110],
        [37.3, 82, 128],
        [36.7, 73, 117],
        [37.0, 75, 120],
        [36.8, 71, 116],
        [37.2, 79, 124],
        [36.9, 72, 118],
        [37.1, 77, 123],
        [36.6, 69, 112],
        [37.3, 81, 127],
        [36.7, 74, 119],
        [37.0, 76, 121],
        [36.8, 70, 114],
        [37.2, 78, 126],
    ]
    health_data = torch.tensor(vital_signs_data, dtype=torch.float32).unsqueeze(0)  # [1, 20, 3]

    # 2. Environmental satellite data tensor
    real_env = fetch_environmental_data(LATITUDE, LONGITUDE)
    sat_tensor = np.zeros((2, 16, 16), dtype=np.float32)
    sat_tensor[0, :, :] = real_env[0]  # temperature
    sat_tensor[1, :, :] = np.mean(real_env[3:6])  # PM10, PM2.5, CO avg
    satellite_data = torch.tensor(sat_tensor).unsqueeze(0)  # [1, 2, 16, 16]

    # 3. Initialize model dynamically based on HEALTH_FEATURES
    model = HybridFusionModel(
        health_input_dim=HEALTH_FEATURES,
        sat_input_channels=2,
        embed_dim=16,
        num_classes=2
    )
    model.eval()

    # 4. Predict
    with torch.no_grad():
        logits = model(health_data, satellite_data)
        probs = torch.softmax(logits, dim=1)
        pred_class = torch.argmax(probs, dim=1)

        print("Logits:", logits)
        print("Softmax probabilities:", probs)
        print("Predicted class:", pred_class)
