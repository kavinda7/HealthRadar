import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from noise import pnoise1

# Configuration
num_patients = 5
num_hours = 7 * 24  # one week
start_time = datetime(2025, 1, 1, 0, 0)

def generate_perlin_series(base, variation, scale=0.05, seed=0):
    return np.array([base + variation * pnoise1(i * scale + seed) for i in range(num_hours)])

# Excel writer
with pd.ExcelWriter("synthetic_patients_data.xlsx", engine="openpyxl") as writer:
    for patient_id in range(num_patients):
        timestamps = [start_time + timedelta(hours=i) for i in range(num_hours)]
        
        # Use patient_id to offset noise seed for uniqueness
        body_temp = generate_perlin_series(36.5, 0.4, scale=0.03, seed=patient_id * 10 + 1)
        pulse = generate_perlin_series(70, 10, scale=0.04, seed=patient_id * 10 + 2)
        spo2 = generate_perlin_series(98, 1.5, scale=0.02, seed=patient_id * 10 + 3)
        resp_rate = generate_perlin_series(16, 3, scale=0.05, seed=patient_id * 10 + 4)
        steps = np.maximum(0, generate_perlin_series(500, 400, scale=0.06, seed=patient_id * 10 + 5)).astype(int)
        sleep_raw = generate_perlin_series(1.0, 1.0, scale=0.01, seed=patient_id * 10 + 6)
        sleep_state = np.digitize(sleep_raw, bins=[0.5, 1.5])

        df = pd.DataFrame({
            "timestamp": timestamps,
            "body_temperature_C": np.round(body_temp, 2),
            "pulse_bpm": np.round(pulse).astype(int),
            "blood_oxygen_percent": np.round(spo2, 1),
            "respiratory_rate": np.round(resp_rate, 1),
            "steps_per_hour": steps,
            "sleep_state": sleep_state
        })

        df.to_excel(writer, sheet_name=str(patient_id), index=False)

print("Synthetic Excel file generated: synthetic_patients_data.xlsx")
