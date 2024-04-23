import requests
import os
import geopandas as gpd
from shapely.geometry import Polygon
import json


def fetch_and_create_shapefile(api_url, district, output_dir="."):
    """
    Fetches geographic data from a specified API and creates a shapefile.
    
    Args:
    api_url (str): URL of the API endpoint to fetch data.
    district (str): A string to identify the district, used in naming the output shapefile.
    output_dir (str): Directory to store the output shapefile. Defaults to the current directory.
    
    Returns:
    None
    """
    # Make a GET request to the API endpoint
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    # Parse JSON response
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Failed to decode JSON from response")
        return

    if 'features' in data:
        features = data['features']
        properties_list = []
        geometry_list = []

        # Process each feature to extract geometry and attributes
        for feature in features:
            attributes = feature['attributes']
            properties_list.append(attributes)
            
            # Construct the geometry using shapely
            if 'geometry' in feature and 'rings' in feature['geometry']:
                polygon = Polygon([tuple(l) for l in feature['geometry']['rings'][0]])
                geometry_list.append(polygon)
            else:
                geometry_list.append(None)

        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(properties_list, geometry=geometry_list)
        if not gdf.empty:
            print(gdf.head())  # Optionally display the first few entries of the GeoDataFrame

            # Create the shapefile files in the specified directory
            shapefile_path = f"{output_dir}/output_shapefile_{district}.shp"
            gdf.to_file(shapefile_path)
            print(f"Shapefile created at {shapefile_path}")
        else:
            print("GeoDataFrame is empty, no shapefile created.")
    else:
        print("No features found in the response")



def get_folder_size(folder_path):
    """
    Calculates the total size of all files in a specified directory.

    Args:
    folder_path (str): The path to the directory whose size you want to calculate.

    Returns:
    int: The total size of the files in the directory in bytes.
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            # Construct full file path
            file_path = os.path.join(dirpath, f)
            # Get file size and add it to total
            total_size += os.path.getsize(file_path)
    return total_size

