from sentinelhub import (
    SHConfig, BBox, CRS, SentinelHubRequest, DataCollection,
    MimeType, bbox_to_dimensions
)
import matplotlib.pyplot as plt
from cdse_config import get_config

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
time_interval = ('2023-06-01', '2023-06-30')

# --- DATA COLLECTION ---
data_collection = DataCollection.define(
    name='cdse_s2_l2a',
    api_id='sentinel-2-l2a',
    service_url='https://sh.dataspace.copernicus.eu'
)

# --- EVALSCRIPT ---
evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B04", "B08"],
    output: { bands: 1 }
  };
}
function evaluatePixel(sample) {
  let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
  return [ndvi];
}
"""

# Request

# Create SentinelHub request
request = SentinelHubRequest(
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=data_collection,
            time_interval=time_interval
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
ndvi_data = request.get_data()[0]

# Visualize the NDVI data

plt.imshow(ndvi_data, cmap='RdYlGn')
plt.colorbar(label='NDVI')
plt.title('NDVI over Budapest')
plt.axis('off')
plt.show()
