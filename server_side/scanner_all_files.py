import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

all_credentials = os.listdir('credentials')

sum_all_size = 0
sum_all_files = 0
for credential in all_credentials:
    # Path to your credentials.json file
    credentials_path = os.path.join('credentials', credential)
    print(credentials_path)

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
            fields='nextPageToken, files(id, name, size, createdTime)'
        ).execute()

        files += response.get('files', [])
        page_token = response.get('nextPageToken')

        if not page_token or len(files) >= max_files:
            break

    if files:
        print(f"sum files: {len(files[:max_files])}")
        sum_size = 0
        for file in files[:max_files]:
            print(f"File name: {file['name'].split('/')[-1]}")
            print(f'size: {(int(file["size"]) / 1024 ** 3):.3f} GB')
            # print(f"https://drive.google.com/file/d/{file['id']}/view")
            print(f"created time: {file['createdTime']}")
            sum_size += int(file["size"])
        print(f'\nall size: {(sum_size / 1024**3):.3f} GB\n')
        sum_all_size += sum_size
        sum_all_files += len(files[:max_files])
    else:
        print("No files found.")

print(f'\nall memory data:\nsum files: {sum_all_files}.\nsum size: {(sum_all_size / 1024**3):.3f} GB')

