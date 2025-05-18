import torch
import numpy as np
from sentinelhub import (
    SHConfig, BBox, CRS, SentinelHubRequest, DataCollection,
    MimeType, bbox_to_dimensions, SentinelHubCatalog
)
import matplotlib.pyplot as plt


def get_sentinel_image_tensor(
    bbox_coords,
    time_start,
    time_end,
    n_images=5,
    max_cloud=20,
    bands=("B03", "B11", "B12"),
    max_dim=512,
    config=None,
    visualize=True
):
    """
    Downloads cloud-free Sentinel-2 images and returns a tensor of shape [1, C, T, H, W].

    Parameters:
        bbox_coords : list     [min_lon, min_lat, max_lon, max_lat]
        time_start   : str     e.g., "2024-08-01"
        time_end     : str     e.g., "2024-10-01"
        n_images     : int     number of time steps to collect
        max_cloud    : int     max cloud % (0-100)
        bands        : tuple   Sentinel-2 band names
        max_dim      : int     max width/height in pixels
        config       : SHConfig or None
        visualize    : bool    whether to show a grid of the images

    Returns:
        torch.Tensor [1, C, T, H, W]
    """
    if config is None:
        from cdse_config import get_config
        config = get_config()

    bbox = BBox(bbox=bbox_coords, crs=CRS.WGS84)

    # Resolution selection
    for res in [10, 20, 60, 100, 300]:
        size = bbox_to_dimensions(bbox, resolution=res)
        if size[0] <= max_dim and size[1] <= max_dim:
            break

    # Data collection
    data_collection = DataCollection.define(
        name="cdse_s2_l2a",
        api_id="sentinel-2-l2a",
        service_url="https://sh.dataspace.copernicus.eu"
    )

    # Get available low-cloud dates
    catalog = SentinelHubCatalog(config=config)
    search_iterator = catalog.search(
        collection=data_collection,
        bbox=bbox,
        time=(time_start, time_end),
        filter={
            "op": "<=",
            "args": [{"property": "eo:cloud_cover"}, max_cloud]
        },
        filter_lang="cql2-json",
        distinct="date"
    )
    available_dates = list(search_iterator)
    selected_dates = available_dates[:n_images]
    if not selected_dates:
        raise ValueError("No cloud-free scenes found in selected range.")

    # Evalscript generation
    evalscript = f"""
    //VERSION=3
    function setup() {{
      return {{
        input: [{', '.join([f'"{b}"' for b in bands])}],
        output: {{ bands: {len(bands)} }}
      }};
    }}
    function evaluatePixel(sample) {{
      return [{', '.join([f'sample.{b}' for b in bands])}];
    }}
    """

    # Download images
    image_stack = []
    for date in selected_dates:
        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[SentinelHubRequest.input_data(
                data_collection=data_collection,
                time_interval=(date, date)
            )],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=bbox,
            size=size,
            config=config
        )
        image = request.get_data()[0]
        image_stack.append(image)

    # Reformat to [1, C, T, H, W]
    stack_array = np.stack(image_stack)  # [T, H, W, C]
    stack_tensor = torch.tensor(stack_array.transpose(0, 3, 1, 2), dtype=torch.float32)  # [T, C, H, W]
    stack_tensor = stack_tensor.permute(1, 0, 2, 3).unsqueeze(0)  # [1, C, T, H, W]


    if visualize:
        rows = (n_images + 2) // 3
        fig, axes = plt.subplots(rows, 3, figsize=(15, 5 * rows))
        for i, (ax, img, date) in enumerate(zip(axes.flat, stack_array, selected_dates)):
            norm_img = np.clip(img / np.max(img), 0, 1)  # img is already [H, W, C]
            ax.imshow(norm_img)
            ax.set_title(f"Date: {date}")
            ax.axis("off")
        for j in range(i + 1, len(axes.flat)):
            axes.flat[j].axis("off")
        plt.tight_layout()
        plt.show()

    return stack_tensor

if __name__ == "__main__":
        sat_tensor = get_sentinel_image_tensor(
            bbox_coords=[24.54, 60.13, 25.15, 60.35],  # Helisinki
            time_start="2024-08-01",
            time_end="2024-10-01",
            n_images=5,
            visualize=True
        )
