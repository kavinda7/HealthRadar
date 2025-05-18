import torch
from hystorical_sentinel import get_sentinel_image_tensor
import matplotlib.pyplot as plt
import numpy as np

def preprocess_satellite_data(
    tensor: torch.Tensor,
    selected_channels: list = None,
    norm_type: str = "zscore"
) -> torch.Tensor:
    """
    Applies channel selection and normalization to satellite data.

    Args:
        tensor: [B, C, T, H, W] input satellite tensor
        selected_channels: list of channel indices to keep (optional)
        norm_type: "zscore" or "minmax"

    Returns:
        torch.Tensor [B, C', T, H, W] processed satellite tensor
    """
    B, C, T, H, W = tensor.shape

    # 1. Channel selection
    if selected_channels is not None:
        tensor = tensor[:, selected_channels, :, :, :]
        C = len(selected_channels)

    # 2. Normalization
    if norm_type == "zscore":
        mean = tensor.mean(dim=(2, 3, 4), keepdim=True)
        std = tensor.std(dim=(2, 3, 4), keepdim=True)
        tensor = (tensor - mean) / (std + 1e-6)

    elif norm_type == "minmax":
        min_val = tensor.amin(dim=(2, 3, 4), keepdim=True)
        max_val = tensor.amax(dim=(2, 3, 4), keepdim=True)
        tensor = (tensor - min_val) / (max_val - min_val + 1e-6)

    else:
        raise ValueError(f"Unknown norm_type: {norm_type}")

    return tensor


if __name__ == "__main__":

    def visualize_satellite_preprocessing(raw: torch.Tensor, processed: torch.Tensor, channel_names=None):
        """
        Plots satellite images before and after preprocessing (per channel, per time).

        Args:
            raw:       [1, C, T, H, W] original tensor
            processed: [1, C, T, H, W] cleaned tensor
            channel_names: list of str optional names for each channel
        """
        _, C, T, H, W = raw.shape
        print(raw.shape)
        channel_names = channel_names or [f"Band {i}" for i in range(C)]

        for c in range(C):
            fig, axes = plt.subplots(2, T, figsize=(3 * T, 6))
            fig.suptitle(f"Channel: {channel_names[c]}", fontsize=16)

            for t in range(T):
                # Raw image
                axes[0, t].imshow(raw[0, c, t].numpy(), cmap="gray")
                axes[0, t].set_title(f"Raw T{t}")
                axes[0, t].axis("off")

                # Processed image
                proc_img = processed[0, c, t].numpy()
                axes[1, t].imshow(proc_img, cmap="gray", vmin=proc_img.min(), vmax=proc_img.max())
                axes[1, t].set_title(f"Processed T{t}")
                axes[1, t].axis("off")


            plt.tight_layout()
            plt.show()


    sat_tensor = get_sentinel_image_tensor(
        bbox_coords=[24.54, 60.13, 25.15, 60.35],  # Helisinki
        time_start="2024-08-01",
        time_end="2024-10-01",
        n_images=5,
        visualize=True
    )

    print(f"sat_tensor.shape: {sat_tensor.shape}")

    # Before: [1, 3, 5, H, W] satellite tensor

    sat_raw = sat_tensor.clone()

    # After processing
    sat_clean = preprocess_satellite_data(sat_raw, selected_channels=[0, 1, 2], norm_type="zscore")
    
    print(f"sat_clean.shape: {sat_clean.shape}")
    
    #len(channel_names) == sat_tensor.shape[1]  # channel count

    # Visualize
    visualize_satellite_preprocessing(sat_raw, sat_clean, channel_names=["B03", "B11", "B12"])
