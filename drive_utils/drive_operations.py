from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# Test Drive API with minimal setup
def minimal_drive_test():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_file(
        'token.json', 
        scopes=['https://www.googleapis.com/auth/drive'])

    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=10, fields="files(id, name)").execute()
    for file in results.get('files', []):
        print(f"Found file: {file.get('name')} with ID: {file.get('id')}")



def list_contents_of_folder(folder_id):
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the full path to the token file
    token_path = os.path.join(dir_path, 'token.json')

    # Use the token to authenticate
    creds = service_account.Credentials.from_service_account_file(
        token_path, 
        scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=creds)

    # List files in the specified folder
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, pageSize=10, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    if files:
        for file in files:
            print(f"Found file: {file.get('name')} with ID: {file.get('id')}")
    else:
        print("No files found in the folder.")



def create_or_find_subfolder(parent_folder_id, subfolder_name):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    # Check if the subfolder exists
    query = f"name = '{subfolder_name}' and '{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])

    if folders:
        print(f"Folder already exists: {folders[0]['name']} with ID: {folders[0]['id']}")
        return folders[0]['id']
    else:
        # Create the subfolder if it does not exist
        file_metadata = {
            'name': subfolder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        print(f"Created folder: {subfolder_name} with ID: {folder.get('id')}")
        return folder.get('id')



def upload_file_to_drive(folder_id, file_path, file_name):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    creds = get_credentials()
    # Initialize the Google Drive API service
    service = build('drive', 'v3', credentials=creds)

    # Prepare the file metadata and the media upload object
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream', resumable=True)

    try:
        # Attempt to upload the file and return the new file ID
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded file with ID: {file.get('id')}")
        return file.get('id')
    except Exception as e:
        # Log any errors that occur during the file upload
        print(f"Failed to upload {file_name}: {e}")
        return None


def get_credentials():
    """Load credentials from a service account JSON file."""
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Construct the full path to the token file
    token_path = os.path.join(dir_path, 'token.json')

    # Use the token to authenticate
    credentials = service_account.Credentials.from_service_account_file(
        token_path, 
        scopes=['https://www.googleapis.com/auth/drive'])

    return credentials

def find_file_id(service, folder_id, file_name):
    """Search for a file by name in a specific folder and return the file ID if it exists."""
    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])
    return files[0]['id'] if files else None


def upload_or_replace_file(folder_id, file_path, file_name, creds):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    service = build('drive', 'v3', credentials=creds)
    file_id = find_file_id(service, folder_id, file_name)
    
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream', resumable=True)

    if file_id:
        # If the file exists, update it
        updated_file = service.files().update(fileId=file_id, body=file_metadata, media_body=media).execute()
        print(f"Updated file with ID: {updated_file.get('id')}")
    else:
        # If the file does not exist, upload it as new
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded new file with ID: {file.get('id')}")
