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

    raw_health = torch.tensor([
        [[36.5, 72, 120], [np.nan, 74, 122], [36.8, 200, 123], [36.6, 73, np.nan], [36.7, 71, 121]],
        [[37.0, 80, 130], [36.9, 79, 128], [np.nan, 300, 127], [37.2, 81, 131], [37.1, 80, 129]]
    ], dtype=torch.float32)

    cleaned_health = preprocess_health_data(raw_health)

    visualize_health_preprocessing(raw_health, cleaned_health, feature_names=["Body Temp", "Pulse", "BP"])

