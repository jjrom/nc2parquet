import sys
import os
import xarray as xr
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon

# Function to create a square polygon from centroid
def create_polygon(lon, lat, grid_size):
    half_size = grid_size / 2
    return Polygon([
        (lon - half_size, lat - half_size),
        (lon + half_size, lat - half_size),
        (lon + half_size, lat + half_size),
        (lon - half_size, lat + half_size),
        (lon - half_size, lat - half_size)  # Close the polygon
    ])
    
GRID_SIZE = os.environ.get('GRID_SIZE', None) # degree grid size
ROOT_DIR = os.environ.get('ROOT_DIR', '/output/')
NETCDF_INPUT_FILE = os.environ.get('NETCDF_INPUT_FILE')
LONGITUDE_DIMENSION = os.environ.get('LONGITUDE_DIMENSION', 'longitude') 
LATITUDE_DIMENSION = os.environ.get('LATITUDE_DIMENSION', 'latitude')
TIME_DIMENSION = os.environ.get('TIME_DIMENSION', 'time')
VARIABLE_NAME = os.environ.get('VARIABLE_NAME', 'value')
NAN_THRESHOLD = os.environ.get('NAN_THRESHOLD', None)

if NETCDF_INPUT_FILE is None:
    if len(sys.argv) > 1:
        NETCDF_INPUT_FILE = sys.argv[1]
    else:
        print("The NETCDF_INPUT_FILE is not set")
        quit()

NETCDF_INPUT_FILE = ROOT_DIR + NETCDF_INPUT_FILE

if not os.path.isfile(NETCDF_INPUT_FILE):
    print(NETCDF_INPUT_FILE + "is not a valid file")
    quit()
    
GEOPARQUET_FILE = os.path.splitext(NETCDF_INPUT_FILE)[0]+'.parquet'
print(f"Converting {NETCDF_INPUT_FILE}  to {GEOPARQUET_FILE}")

# Load NetCDF using lazy loading (avoids memory issues)
ds = xr.open_dataset(NETCDF_INPUT_FILE, chunks="auto")

# Extract value
value = ds[VARIABLE_NAME].load()  # Load only required data

# Convert to Pandas DataFrame
df = value.to_dataframe().reset_index()

# Fast Filtering: Remove NaN & almost zero values
if NAN_THRESHOLD is not None:
    mask = (df[VARIABLE_NAME] <= NAN_THRESHOLD) & (~np.isnan(df[VARIABLE_NAME]))
else:
    mask = ~np.isnan(df[VARIABLE_NAME])
df = df[mask]

# Vectorized Geometry Conversion
if GRID_SIZE is None:
    df["geometry"] = gpd.points_from_xy(df[LONGITUDE_DIMENSION], df[LATITUDE_DIMENSION])
else:
    # Apply function to create geometry column
    df['geometry'] = df.apply(lambda row: create_polygon(row[LONGITUDE_DIMENSION], row[LATITUDE_DIMENSION], GRID_SIZE), axis=1)

# Convert to GeoDataFrame with proper CRS
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

# Select required columns and map it to generic geometry/time/value
gdf = gdf[["geometry", TIME_DIMENSION, VARIABLE_NAME]]
gdf.columns = ["geometry", "time", "value"]

# Save to GeoParquet
gdf.to_parquet(GEOPARQUET_FILE, engine="pyarrow", index=False)  # Setting index=False to get True GeoParquet

print(f"✅ Successfully saved single GeoParquet file: {GEOPARQUET_FILE}")

