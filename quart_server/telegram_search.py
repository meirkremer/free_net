import re
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.utils import get_peer_id
from config import private_config


def clean_name(file_name: str):
    base_name = (''.join(file_name.split('.')[:-1]) if '.' in file_name else file_name).replace('_', ' ')
    return base_name


def remove_unwanted_chars(input_string: str):
    input_string = input_string.replace('_', ' ')
    pattern = r'[^a-zA-Z\d.א-ת\s]'
    clean_string = re.sub(pattern, '', input_string)
    remove_extra_space = ' '.join(clean_string.split())
    if len(remove_extra_space) < 1:
        remove_extra_space = "None"
    return remove_extra_space


async def search_files(search_query: str, search_type: str):
    api_id = private_config['api_id']
    api_hash = private_config['api_hash']
    string_auth = private_config['string_auth']
    all_matches = {}
    async with TelegramClient(StringSession(string_auth), api_id, api_hash) as client:
        async for message in client.iter_messages(entity='', search=search_query):
            if message.file and message.file.mime_type.startswith(search_type):
                file_name = message.file.name
                if file_name is None:
                    file_name = 'אין שם'
                file_name = clean_name(remove_unwanted_chars(file_name))
                message_id = message.id
                channel_id = get_peer_id(message.peer_id)
                video_size = f"{(message.file.size / 1024 ** 3):.3f} GB"
                file_id = f"{channel_id}###{message_id}"
                all_matches[file_id] = file_name, video_size

    return all_matches
