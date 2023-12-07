import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta


def get_all_drive_files(service: build):
    files = []
    page_token = None
    while True:
        response = service.files().list(
            pageSize=1000,  # The Maximum page size is 1000
            pageToken=page_token,
            fields='nextPageToken, files(id, name, createdTime)'
        ).execute()

        files += response.get('files', [])
        page_token = response.get('nextPageToken')

        if not page_token:
            break

    if not files:
        print('no files found')

    return files


def get_files_to_delete(all_files: list, delete_time) -> list:
    delete_list = []
    for file in all_files:
        str_time = file['createdTime']
        datetime_object = datetime.strptime(str_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        if datetime_object < delete_time:
            delete_list.append(file['id'])

    if len(delete_list) == 0:
        print(f'no files to delete from {len(all_files)} files')

    return delete_list


def remove_old_files(cred_path: str, delete_time: datetime):
    # Authenticate and create a service client
    credentials = service_account.Credentials.from_service_account_file(cred_path,
                                                                        scopes=[
                                                                            'https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=credentials)

    # get all files stored on this account
    files = get_all_drive_files(service)
    if not files:
        return None

    # get a list of files id to delete
    delete_list = get_files_to_delete(files, delete_time)
    if not delete_list:
        return None

    # Delete the files
    for file_id in delete_list:
        service.files().delete(fileId=file_id).execute()

    # clean trash
    service.files().emptyTrash().execute()
    print(f'{len(delete_list)} files deleted successfully!')


def main():
    files_life_time = timedelta(days=1)
    delete_time = datetime.now() - files_life_time
    credentials_dir = 'credentials'
    credentials_files = os.listdir(credentials_dir)
    for credential_file in credentials_files:
        credentials_path = os.path.join(credentials_dir, credential_file)
        remove_old_files(credentials_path, delete_time)


if __name__ == '__main__':
    main()
