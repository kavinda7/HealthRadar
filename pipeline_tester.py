import requests
import torch
import numpy as np
from hybrid_fusion_pipeline import HybridFusionModel  # improved version

# --- Constants ---
LATITUDE = 47.4979
LONGITUDE = 19.0402
HEALTH_FEATURES = 3
SAT_CHANNELS = 2
SAT_HISTORY_DAYS = 14  # past 14 days
SAT_H, SAT_W = 16, 16

# --- Fake Time-Series Satellite Sequence Generator ---
def fetch_satellite_sequence(lat, lon, days=14):
    real = fetch_environmental_data(lat, lon)

    # Simulate satellite history by jittering current value
    seq = []
    for t in range(days):
        daily = np.zeros((SAT_CHANNELS, SAT_H, SAT_W), dtype=np.float32)
        daily[0] = real[0] + np.random.normal(0, 0.2)  # temperature
        daily[1] = np.mean(real[3:6]) + np.random.normal(0, 1.0)  # pollution
        seq.append(daily)
    return torch.tensor(seq).permute(1, 0, 2, 3).unsqueeze(0)  # [1, C, T, H, W]

# --- Live API for real env values ---
def fetch_environmental_data(lat, lon):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
    weather = requests.get(weather_url).json()["hourly"]
    air = requests.get(air_url).json()["hourly"]

    return [
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

# --- Main ---
if __name__ == "__main__":
    # Health data (20 records × 3 features)
    vital_signs_data = [
        [36.7, 72, 118], [37.0, 76, 122], [36.8, 70, 115], [37.2, 80, 125],
        [36.9, 74, 119], [37.1, 78, 121], [36.6, 68, 110], [37.3, 82, 128],
        [36.7, 73, 117], [37.0, 75, 120], [36.8, 71, 116], [37.2, 79, 124],
        [36.9, 72, 118], [37.1, 77, 123], [36.6, 69, 112], [37.3, 81, 127],
        [36.7, 74, 119], [37.0, 76, 121], [36.8, 70, 114], [37.2, 78, 126]
    ]
    health_data = torch.tensor(vital_signs_data, dtype=torch.float32).unsqueeze(0)  # [1, 20, 3]

    # Simulated historical satellite sequence
    satellite_data = fetch_satellite_sequence(LATITUDE, LONGITUDE, SAT_HISTORY_DAYS)  # [1, 2, 14, 16, 16]

    # Initialize updated model
    model = HybridFusionModel(
        health_input_dim=HEALTH_FEATURES,
        sat_input_channels=SAT_CHANNELS,
        embed_dim=16,
        num_classes=2
    )
    model.eval()

    with torch.no_grad():
        logits = model(health_data, satellite_data)
        probs = torch.softmax(logits, dim=1)
        pred_class = torch.argmax(probs, dim=1)

        print("Logits:", logits)
        print("Softmax probabilities:", probs)
        print("Predicted class:", pred_class)
