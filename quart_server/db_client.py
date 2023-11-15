import json

import requests

MAIN_URL = 'http://127.0.0.1:5010'


def check_user(user_email: str) -> bool:
    rout = MAIN_URL + '/check-user'
    par = {
        'user_email': user_email
    }
    response = requests.get(rout, params=par)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False


def insert_user(user_name: str, user_email: str) -> bool:
    rout = MAIN_URL + '/insert-user'
    data = {
        'user_name': user_name,
        'user_email': user_email
    }
    response = requests.post(rout, json=data)
    if response.status_code == 200:
        return True
    elif response.status_code == 409:
        return False


def delete_user(user_email: str) -> bool:
    rout = MAIN_URL + '/delete-user'
    data = {
        'user_email': user_email
    }
    response = requests.post(rout, json=data)
    if response.status_code == 200:
        return True
    return False


def insert_search(user_email: str, search_query: str, date_time: str) -> bool:
    rout = MAIN_URL + '/insert-search'
    data = {
        'user_email': user_email,
        'search_query': search_query,
        'date_time': date_time
    }
    response = requests.post(rout, json=data)
    if response.status_code == 200:
        return True


def insert_download(user_email: str, file_name: str, file_size: int, date_time: str) -> bool:
    rout = MAIN_URL + '/insert-download'
    data = {
        'user_email': user_email,
        'file_name': file_name,
        'file_size': file_size,
        'date_time': date_time
    }
    response = requests.post(rout, json=data)
    if response.status_code == 200:
        return True


def fetch_search(user_email: str) -> dict:
    rout = MAIN_URL + '/fetch-search'
    par = {
        'user_email': user_email
    }
    response = requests.get(rout, params=par)
    if response.status_code == 200:
        return json.loads(response.content)


def fetch_download(user_email: str) -> dict:
    rout = MAIN_URL + '/fetch-download'
    par = {
        'user_email': user_email
    }
    response = requests.get(rout, params=par)
    if response.status_code == 200:
        return json.loads(response.content)
