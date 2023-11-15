import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Path to your credentials.json file
credentials_files = os.listdir('credentials')
for credential_file in credentials_files:
    print(credential_file)
    credentials_path = os.path.join('credentials', credential_file)
    # Maximum number of files to retrieve
    max_files = 3000

    # Authenticate and create a service client
    credentials = service_account.Credentials.from_service_account_file(credentials_path,
                                                                        scopes=[
                                                                            'https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=credentials)

    files = []
    page_token = None

    while True:
        response = service.files().list(
            pageSize=1000,  # Maximum page size is 1000
            pageToken=page_token,
            fields='nextPageToken, files(id, name, createdTime)'
        ).execute()

        files += response.get('files', [])
        page_token = response.get('nextPageToken')

        if not page_token or len(files) >= max_files:
            break

    now = datetime.now()
    life_hours = timedelta(hours=24)
    delete_time = now - life_hours
    print(delete_time)
    delete_list = []
    if files:
        print(f"sum files: {len(files)}")
        for file in files:
            str_time = file['createdTime']
            datetime_object = datetime.strptime(str_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            print(f"File name: {file['name']}")
            # print(f"https://drive.google.com/file/d/{file['id']}/view")
            print(f"created time: {datetime_object}")
            if datetime_object < delete_time:
                delete_list.append(file['id'])
    else:
        print("No files found.")

    # Delete the file
    for file_id in delete_list:
        service.files().delete(fileId=file_id).execute()

    # clean trash
    service.files().emptyTrash().execute()

