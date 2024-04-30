
from drive_utils.settings import FOLDER_ID
from drive_utils.data_processing import fetch_and_create_shapefile
from drive_utils import drive_operations

parent_folder_id = FOLDER_ID


api_urls = {
    "assembly": 'https://maps.lacity.org/lahub/rest/services/Boundaries/MapServer/2/query?where=1%3D1&outFields=*&outSR=4326&f=json',
    "bids_city_clerk": 'https://services5.arcgis.com/7nsPwEMP38bSkCjy/arcgis/rest/services/Business_Improvement_Districts/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
    "city_council": 'https://maps.lacity.org/lahub/rest/services/Boundaries/MapServer/13/query?where=1%3D1&outFields=*&outSR=4326&f=json',
    "congressional": 'https://arcgis.gis.lacounty.gov/arcgis/rest/services/LACounty_Dynamic/Political_Boundaries/MapServer/2/query?where=1%3D1&outFields=*&outSR=4326&f=json',
    "neighborhood_council": 'https://services5.arcgis.com/7nsPwEMP38bSkCjy/arcgis/rest/services/Neighborhood_Council_Boundaries_(2018)/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
    "senate": 'https://maps.lacity.org/lahub/rest/services/Boundaries/MapServer/23/query?where=1%3D1&outFields=*&outSR=4326&f=json',
    "supervisors": 'https://maps.lacity.org/lahub/rest/services/Boundaries/MapServer/4/query?where=1%3D1&outFields=*&outSR=4326&f=json'
}

# for district, api_url in api_urls.items():
#     fetch_and_create_shapefile(api_url, district, parent_folder_id)
    
print(drive_operations.list_files_in_folder(parent_folder_id))
