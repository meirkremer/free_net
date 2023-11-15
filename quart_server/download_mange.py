from telethon import TelegramClient
from telethon.sessions import StringSession
from config import private_config as conf
from chunk_mange import StoreChunk


class DownloadFile:
    def __init__(self, file_id: str, store_chunk: StoreChunk):
        self._client = TelegramClient(StringSession(conf['string_auth']), conf['api_id'], conf['api_hash'])
        self._channel_id, self._message_id = [int(number) for number in file_id.split('###')]
        self._chunk_store = store_chunk

    async def connect_client(self):
        await self._client.connect()

    async def disconnect_client(self):
        await self._client.disconnect()

    async def get_file_message(self) -> tuple:
        channel = await self._client.get_entity(self._channel_id)
        file_message = await self._client.get_messages(channel, ids=self._message_id)

        # Extract the data from the message
        file_name = file_message.file.name if file_message.file.name else f'untitled{file_message.file.ext}'
        file_size = file_message.file.size
        mime_type = file_message.file.mime_type

        return file_message, file_name, file_size, mime_type

    async def download_file(self, file_message):
        async for chunk in self._client.iter_download(file_message):
            self._chunk_store.insert_chunk(chunk)
        self._chunk_store.insert_chunk(None)
