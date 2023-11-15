import os
import re
import time
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from chunk_mange import StoreChunk


class UploadFile:
    """
    Upload file in chunks into google drive.
    """
    def __init__(self, file_name: str, file_size: int, mime_type: str, chunk_store: StoreChunk):
        self._file_name = self._get_clean_name(file_name)
        self._file_size = file_size
        self._file_mime_type = mime_type
        self._chunk_store = chunk_store
        self._credentials = self._get_open_drive_account(self._file_size)
        self._access_token = self._get_token(self._credentials)
        self._CHUNK_SIZE = 10

    @staticmethod
    def _get_clean_name(file_name: str) -> str:
        input_string = file_name.replace('_', ' ')
        pattern = r'[^a-zA-Z\d.א-ת\s]'
        clean_string = re.sub(pattern, '', input_string)
        if len(clean_string) < 1:
            clean_string = "None"
        return clean_string

    @staticmethod
    def _get_free_drive_store(credential_file_path: str) -> int:
        credentials = Credentials.from_service_account_file(credential_file_path)
        drive_service = build('drive', 'v3', credentials=credentials)

        # Retrieve the user's storage quota information
        about = drive_service.about().get(fields='storageQuota').execute()

        # Get the total storage space in bytes
        total_storage = int(about['storageQuota']['limit'])

        # Get the used storage space in bytes
        used_storage = int(about['storageQuota']['usage'])
        return total_storage - used_storage

    def _get_open_drive_account(self, file_size: int) -> str | bool:
        credentials_files = os.listdir('credentials')
        for credential_file in credentials_files:
            clean_store = self._get_free_drive_store(os.path.join('credentials', credential_file))
            if file_size + 1024 > clean_store:
                continue
            return os.path.join('credentials', credential_file)
        return False

    @staticmethod
    def _get_token(json_path: str) -> str:

        # Load credentials from the JSON file
        creds = service_account.Credentials.from_service_account_file(
            json_path,
            scopes=['https://www.googleapis.com/auth/drive']  # Adjust the scope as needed
        )

        request = Request()

        # Manually trigger the authorization flow if needed
        if not creds.valid:
            creds.refresh(request)

        # Access token
        access_token = creds.token
        return access_token

    def _create_file_head(self) -> str:
        # Create the upload session
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json',
        }

        data = {
            'name': self._file_name,
            'mimeType': self._file_mime_type
        }

        response = requests.post(
            'https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable',
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            return response.headers['Location']
        else:
            raise Exception(f'file head created failed. response code: {response.status_code}')

    def _upload_file_content(self, location: str) -> None:
        chunk_size = self._CHUNK_SIZE * 512 * 1024
        start_byte = 0
        progress = True
        while progress:
            chunk, progress = self._chunk_store.fetch_chunks(self._CHUNK_SIZE)
            if not chunk:
                time.sleep(1)
                continue
            end_byte = min(start_byte + chunk_size, self._file_size)
            content_range = f'bytes {start_byte}-{end_byte - 1}/{self._file_size}'
            headers = {
                'Authorization': f'Bearer {self._access_token}',
                'Content-Range': content_range,
            }

            response = requests.put(
                location,
                headers=headers,
                data=chunk
            )
            if response.status_code == 308:
                start_byte = end_byte
            elif response.status_code != 200:
                raise Exception(f'en error happened during the upload status code: {response.status_code}'
                                f'\n{response.headers}')

    def _finish_upload(self, location: str) -> str:
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Range': f'bytes */{self._file_size}',  # Indicates completion
        }
        response = requests.put(
            location,
            headers=headers
        )

        if response.status_code == 200:
            # Retrieve the file ID of the uploaded file
            response_data = response.json()
            file_id = response_data.get('id')

            # Set permissions for the file
            permission = {
                'type': 'anyone',
                'role': 'reader',
            }

            credentials = service_account.Credentials.from_service_account_file(
                self._credentials,
                scopes=['https://www.googleapis.com/auth/drive']
            )
            drive_service = build('drive', 'v3', credentials=credentials)

            drive_service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
            return file_id

    def run_upload(self) -> tuple:
        location = self._create_file_head()
        time.sleep(2)
        self._upload_file_content(location)
        return self._finish_upload(location), self._file_name
