import asyncio
import concurrent.futures
import logging
import time
from email_mange import send_email
from datetime import datetime, timedelta
from db_client import insert_download
from chunk_mange import StoreChunk
from upload_mange import UploadFile
from download_mange import DownloadFile


class GetFiles:
    logging.basicConfig(level=logging.INFO, filename='log/get_file.log', filemode='w')

    def __init__(self, file_ids: list, email: str):
        self._file_ids = file_ids
        self._email = email

    async def _get_file(self, file_id: str):
        start_time = time.time()

        # create store instance
        file_chunk = StoreChunk()

        # create downloader instance
        downloader = DownloadFile(file_id, file_chunk)
        await downloader.connect_client()

        # get the file message and file data
        file_message, file_name, file_size, mime_type = await downloader.get_file_message()

        # create uploader instance
        uploader = UploadFile(file_name, file_size, mime_type, file_chunk)

        # create looper for upload in background
        looper = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            data = looper.run_in_executor(executor, uploader.run_upload)
            await downloader.download_file(file_message)
            print('end download')
            await downloader.disconnect_client()
        print('done')
        file_id, file_name = await data
        print(file_id)
        print(file_name)

        # send link to the user
        send_email(file_id, file_name, self._email)

        # insert download to db
        try:
            insert_download(self._email, file_name, file_message.file.size,
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            logging.error(e)
        run_time = timedelta(seconds=(time.time() - start_time))
        logging.info(f'[{datetime.now()}] {file_name = } size: {(file_size / 1024 ** 3):.3f} run time: {run_time}')

    async def get_files(self):
        for file_id in self._file_ids:
            await self._get_file(file_id)
