from sentinelhub import (
    SHConfig, BBox, CRS, SentinelHubRequest, DataCollection, MimeType,
    bbox_to_dimensions, SentinelHubCatalog
)
import torch
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from cdse_config import get_config

# --- Parameters ---
N_IMAGES = 5
LATLON_BBOX = [19.00, 47.35, 19.10, 47.45]  # Budapest
TIME_START = "2024-08-01"
TIME_END = "2024-10-01"
MAX_CLOUD = 20  # %

# --- Config ---
config = get_config()
bbox = BBox(bbox=LATLON_BBOX, crs=CRS.WGS84)

# --- Resolution ---
MAX_DIM = 512
for res in [10, 20, 60, 100, 300]:
    size = bbox_to_dimensions(bbox, resolution=res)
    if size[0] <= MAX_DIM and size[1] <= MAX_DIM:
        selected_resolution = res
        break

# --- Data collection ---
data_collection = DataCollection.define(
    name="cdse_s2_l2a",
    api_id="sentinel-2-l2a",
    service_url="https://sh.dataspace.copernicus.eu"
)

# --- Catalog search using CQL2 filter ---
catalog = SentinelHubCatalog(config=config)

search_iterator = catalog.search(
    collection=data_collection,
    bbox=bbox,
    time=(TIME_START, TIME_END),
    filter={
        "op": "<=",
        "args": [
            {"property": "eo:cloud_cover"},
            MAX_CLOUD
        ]
    },
    filter_lang="cql2-json",
    distinct="date"
)

for i, item in enumerate(search_iterator):
    print(f"[{i}] Type: {type(item)}")
    print("Sample item:", str(item)[:300], "\n")  # print a short preview
    if i >= 2: break


# Items are already dates in string form like "2024-09-30"
available_dates = list(search_iterator)  # No parsing needed
selected_dates = available_dates[:N_IMAGES]

print(f"Selected {len(selected_dates)} cloud-free dates:\n{selected_dates}")


# --- Evalscript (B03, B11, B12) ---
evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B03", "B11", "B12"],
    output: { bands: 3 }
  };
}
function evaluatePixel(sample) {
  return [sample.B03, sample.B11, sample.B12];
}
"""

# --- Download image stack ---
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
    image = request.get_data()[0]  # (H, W, 3)
    image_stack.append(image)
    print(f"Fetched image for {date}")

stack_array = np.stack(image_stack)
# --- Reformat to [B, C, T, H, W] ---
stack_array = stack_array.transpose(0, 3, 1, 2)  # [T, C, H, W]
stack_tensor = torch.tensor(stack_array).unsqueeze(0).float()  # [1, C, T, H, W]

print(f"\nHybridFusion input shape: {stack_tensor.shape} [B, C, T, H, W]")


# --- Visualize all images ---
rows = (N_IMAGES + 2) // 3  # 3 images per row
fig, axes = plt.subplots(rows, 3, figsize=(15, 5 * rows))

for i, (ax, img, date) in enumerate(zip(axes.flat, stack_array, selected_dates)):
    norm_img = np.clip(img.transpose(1, 2, 0) / np.max(img), 0, 1)
    ax.imshow(norm_img)
    ax.set_title(f"Date: {date}")
    ax.axis("off")

# Hide any unused subplots
for j in range(i + 1, len(axes.flat)):
    axes.flat[j].axis("off")

plt.tight_layout()
plt.show()

