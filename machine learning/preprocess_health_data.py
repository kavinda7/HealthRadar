import numpy as np
import torch
import pandas as pd
import matplotlib.pyplot as plt

def preprocess_health_data(raw_tensor: torch.Tensor, outlier_z=3.0) -> torch.Tensor:
    """
    Cleans health data: handles missing values (NaNs), removes outliers, normalizes per user.
    
    Args:
        raw_tensor: [B, T, F] – raw health data (may contain NaNs)
        outlier_z: float – z-score threshold for outlier removal (default: 3.0)
    
    Returns:
        torch.Tensor of shape [B, T, F] – cleaned and normalized
    """
    B, T, F = raw_tensor.shape
    processed = []

    for b in range(B):
        df = pd.DataFrame(raw_tensor[b].numpy(), columns=[f'feat_{i}' for i in range(F)])

        # 1. Missing value imputation
        df = df.interpolate(limit_direction="both", method="linear")
        df = df.bfill().ffill()

        # 2. Outlier removal (z-score)
        z = (df - df.mean()) / df.std()
        df[z.abs() > outlier_z] = np.nan

        # 3. Impute again after outlier removal
        df = df.interpolate(limit_direction="both", method="linear")
        df = df.bfill().ffill()

        # 4. Per-user (per-batch) normalization
        normed = (df - df.mean()) / df.std()
        processed.append(normed.to_numpy())

    return torch.tensor(np.stack(processed), dtype=torch.float32)

def downsample_health_to_satellite_times(
    health_df: pd.DataFrame,
    satellite_times: list,
    window: str = "12h"
) -> torch.Tensor:
    """
    Aligns health time-series to satellite timestamps by averaging over a time window.

    Args:
        health_df        : pd.DataFrame with datetime index and health features
        satellite_times  : list of str or pd.Timestamp, satellite image timestamps
        window           : str, aggregation window (e.g. '12h' means ±6h around each timestamp)

    Returns:
        torch.Tensor: shape [1, T, F] where T = len(satellite_times), F = feature count
    """
    downsampled = []

    half_window = pd.Timedelta(window) / 2
    health_df = health_df.sort_index()

    for t in satellite_times:
        t = pd.to_datetime(t)
        segment = health_df.loc[t - half_window : t + half_window]

        if segment.empty:
            #raise ValueError(f"No health data found near satellite timestamp {t}")
            print(f"Skipping {t} no data in window")
            continue

        
        vector = segment.mean().to_numpy()
        downsampled.append(vector)

    result = torch.tensor(downsampled, dtype=torch.float32).unsqueeze(0)  # [1, T, F]
    return result


if __name__ == "__main__":

    def visualize_health_preprocessing(raw: torch.Tensor, cleaned: torch.Tensor, feature_names=None):
        """
        Plots before and after preprocessing for each user and feature.

        Args:
            raw:     [B, T, F] raw tensor
            cleaned: [B, T, F] processed tensor
            feature_names: list of feature names (optional)
        """
        B, T, F = raw.shape
        feature_names = feature_names or [f"Feature {i}" for i in range(F)]

        for b in range(B):
            fig, axes = plt.subplots(F, 1, figsize=(10, 3 * F))
            fig.suptitle(f"User {b}", fontsize=16)

            for f in range(F):
                ax = axes[f] if F > 1 else axes
                raw_series = raw[b, :, f].numpy()
                clean_series = cleaned[b, :, f].numpy()

                ax.plot(raw_series, label="Raw", color="red", linestyle="--", marker="o")
                ax.plot(clean_series, label="Cleaned", color="green", marker="x")
                ax.set_title(feature_names[f])
                ax.legend()
                ax.grid(True)

            plt.tight_layout()
            plt.show()

    dates = pd.date_range("2024-08-05", periods=50, freq="6h")
    health_df = pd.DataFrame({
        "temp": [36.5, np.nan, 36.8, 36.6, 36.7, 36.9, 37.0, np.nan, 37.1, 36.8,
                36.5, np.nan, 36.8, 36.6, 36.7, 36.9, 37.0, np.nan, 37.1, 36.8,
                36.5, np.nan, 36.8, 36.6, 36.7, 36.9, 37.0, np.nan, 37.1, 36.8,
                36.5, np.nan, 36.8, 36.6, 36.7, 36.9, 37.0, np.nan, 37.1, 36.8,
                36.5, np.nan, 36.8, 36.6, 36.7, 36.9, 37.0, np.nan, 37.1, 36.8],
        
        "hr":   [72, 74, 200, 73, 71, 75, 76, 300, 77, 78,
                72, 74, 200, 73, 71, 75, 76, 300, 77, 78,
                72, 74, 200, 73, 71, 75, 76, 300, 77, 78,
                72, 74, 200, 73, 71, 75, 76, 300, 77, 78,
                72, 74, 200, 73, 71, 75, 76, 300, 77, 78],

        "bp":   [120, 122, 123, np.nan, 121, 125, 127, 126, 129, 128,
                120, 122, 123, np.nan, 121, 125, 127, 126, 129, 128,
                120, 122, 123, np.nan, 121, 125, 127, 126, 129, 128,
                120, 122, 123, np.nan, 121, 125, 127, 126, 129, 128,
                120, 122, 123, np.nan, 121, 125, 127, 126, 129, 128]
    }, index=dates)


    cleaned_tensor = preprocess_health_data(torch.tensor(health_df.to_numpy()).unsqueeze(0))  # [1, T, F]
    cleaned_df = pd.DataFrame(cleaned_tensor.squeeze(0).numpy(), index=dates, columns=health_df.columns)


    visualize_health_preprocessing(
        torch.tensor(health_df.to_numpy()).unsqueeze(0),
        torch.tensor(cleaned_df.to_numpy()).unsqueeze(0),
        feature_names=["Body Temp", "Pulse", "BP"]
    )

    print("Health tensor shape:", cleaned_tensor.shape)  # [1, T, F]
    print(cleaned_tensor)

    health_tensor = downsample_health_to_satellite_times(
        cleaned_df,
        ["2024-08-05", "2024-08-10", "2024-08-15"],
        window="12h"
    )

    print("Downsampled health tensor shape:", health_tensor.shape)  # [1, T, F]
    print(health_tensor)