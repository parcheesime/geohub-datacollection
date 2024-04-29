import requests
import json
import geopandas as gpd
from shapely.geometry import Polygon
from drive_utils import drive_operations
from google.oauth2 import service_account
import os
import tempfile


def fetch_and_create_shapefile(api_url, district, parent_folder_id):
    """
    Fetches geographic data from a specified API, creates a shapefile, and saves it to Google Drive in a district-specific subfolder.
    
    Args:
    api_url (str): URL of the API endpoint to fetch data.
    district (str): District identifier used in naming the output shapefile and subfolder.
    parent_folder_id (str): Google Drive folder ID where the district subfolders are located.
    
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
                print(gdf.head())  # Display some entries for logging

                creds = drive_operations.get_credentials()
                district_folder_id = drive_operations.create_or_find_subfolder(parent_folder_id, district)

                # Temporarily save the shapefile locally in the /tmp directory
                with tempfile.TemporaryDirectory() as tmpdir:
                    shapefile_base_path = os.path.join(tmpdir, f"{district}.shp")
                    gdf.to_file(shapefile_base_path, driver='ESRI Shapefile')
                    
                    # Upload each generated file component to Google Drive
                    for file_name in os.listdir(tmpdir):
                        file_path = os.path.join(tmpdir, file_name)
                        if os.path.isfile(file_path):  # Ensure it's a file
                            drive_operations.upload_file_to_drive(district_folder_id, file_path, file_name)

                print(f"Shapefiles for district {district} successfully uploaded to Google Drive.")


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


def fetch_and_create_shapefile_show(api_url, district):
    """
    Fetches geographic data from a specified API and creates a shapefile.
    
    Args:
    api_url (str): URL of the API endpoint to fetch data.
    district (str): A string to identify the district, used in naming the output shapefile.
    output_dir (str): Directory to store the output shapefile. Defaults to the current directory.
    
    Returns:
    str: String representation of the head of the GeoDataFrame.
    """
    # Make a GET request to the API endpoint
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

    # Parse JSON response
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Failed to decode JSON from response")
        return None

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
            gdf_head = gdf.head().to_string()  # Convert head to string
            return district, gdf_head
        else:
            print("GeoDataFrame is empty, no shapefile created.")
            return None
    else:
        print("No features found in the response")
        return None