import torch
import numpy as np
import matplotlib.pyplot as plt
from sentinelhub import (
    SHConfig, BBox, CRS, SentinelHubRequest, DataCollection,
    MimeType, bbox_to_dimensions, SentinelHubCatalog
)
from hybrid_fusion_pipeline import HybridFusionModel
from hystorical_satellite_fetcher import get_sentinel_image_tensor
from preprocess_satellite_data import preprocess_satellite_data
from preprocess_health_data import preprocess_health_data, downsample_health_to_satellite_times

# --- Entry point ---
if __name__ == "__main__":
    # Step 1: Fetch satellite data tensor [1, C, T, H, W]
    sat_raw = get_sentinel_image_tensor(
        bbox_coords=[19.00, 47.35, 19.10, 47.45],  # Budapest
        time_start="2024-08-01",
        time_end="2024-10-01",
        n_images=5,
        visualize=True
    )

    sat_clean = preprocess_satellite_data(sat_raw, selected_channels=[0, 1, 2], norm_type="zscore")

    # Step 2: Generate dummy health data [1, T, F]
    B, C, T, H, W = sat_clean.shape
    HEALTH_FEATURES = 3
    health_raw = torch.randn(B, T, HEALTH_FEATURES)

    health_clean = preprocess_health_data(health_raw)
    #downsample_health_to_satellite_times

    # Step 3: Create and run model
    model = HybridFusionModel(
        health_input_dim=HEALTH_FEATURES,
        sat_input_channels=C,
        embed_dim=16,
        num_classes=2
    )
    model.eval()

    with torch.no_grad():
        output = model(health_clean, sat_clean)
        probs = torch.softmax(output, dim=1)
        pred = torch.argmax(probs, dim=1)

        print("Logits:", output)
        print("Probabilities:", probs)
        print("Predicted class:", pred)
