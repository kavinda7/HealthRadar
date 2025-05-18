from sentinelhub import (
    SHConfig, BBox, CRS, SentinelHubRequest, DataCollection,
    MimeType, bbox_to_dimensions
)
import matplotlib.pyplot as plt
from cdse_config import get_config
import numpy as np

# Print the available data collections
print([dc for dc in DataCollection.get_available_collections()])

# Load the configuration from a separate file
config = get_config()

# --- AREA and RESOLUTION ---
bbox = BBox(bbox=[58.50, 15.10, 70.50, 30.00], crs=CRS.WGS84)

MAX_DIM = 2500  # maximum allowed pixels per side

# Try from 10m resolution and go coarser until under limit
for res in [10, 20, 60, 100, 200, 300, 500, 1000, 2000]:
    size = bbox_to_dimensions(bbox, resolution=res)
    if size[0] <= MAX_DIM and size[1] <= MAX_DIM:
        selected_resolution = res
        break
else:
    raise ValueError(f"Area too large even at {res}m resolution.")

print(f"Using resolution: {selected_resolution}m → final size: {size}")

# --- TIME INTERVAL ---
time_interval = ('2023-05-01', '2023-06-30')


data_collection = DataCollection.define(
    name='cdse_s1_grd',
    api_id='sentinel-1-grd',
    service_url='https://sh.dataspace.copernicus.eu'
)

# --- EVALSCRIPT ---
evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["VV"],
    output: { bands: 1, sampleType: "FLOAT32" }
  };
}
function evaluatePixel(sample) {
  let db = 10 * Math.log10(sample.VV);
  if (!isFinite(db)) return [0];
  return [Math.max(-20, Math.min(5, db))];
}
"""


# Request

# Create SentinelHub request
request = SentinelHubRequest(
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=data_collection,
            time_interval=time_interval,
            mosaicking_order='mostRecent'
        )
    ],
    responses=[
        SentinelHubRequest.output_response("default", MimeType.TIFF)
    ],
    bbox=bbox,
    size=size, #=bbox_to_dimensions(bbox, resolution=10),
    config=config
)

# Download and get the result
s1_data  = request.get_data()[0]

# Visualize the NDVI data

# Rescale for better contrast: normalize between -20 and +5 dB
s1_data_clipped = np.clip(s1_data, -20, 5)
s1_normalized = (s1_data_clipped + 20) / 25  # scale to 0–1

plt.imshow(s1_normalized, cmap='gray')
plt.title('Sentinel-1 VV Backscatter (dB)')
plt.colorbar(label='Scaled intensity')
plt.axis('off')
plt.show()
