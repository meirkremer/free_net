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


def daily_summary():
    rout = MAIN_URL + '/daily-summary'
    response = requests.get(rout)
    response = json.loads(response.content)
    return response


def use_summary():
    rout = MAIN_URL + '/use-summery'
    response = requests.get(rout)
    response = json.loads(response.content)

    return response


def user_summary(user_email):
    rout = MAIN_URL + f'/user-summary/{user_email}'
    response = requests.get(rout)
    response = json.loads(response.content)

    return response


def print_use_summary():
    response = use_summary()
    print(type(response))
    print(response)
    sum_search = response.get('sum_searches')
    sum_downloads = response.get('sum_downloads')
    downloads_size = response.get('all_downloads_size')

    print(f'free net use summary:\nsearches: {sum_search}\ndownloads: {sum_downloads}\n'
          f'all files size: {downloads_size:.3f} GB')


def print_user_summary(user_email):
    response = user_summary(user_email)
    sum_size = 0
    for key in response:
        download = response[key]
        sum_size += int(download.get("file_size"))
        print(f'file name: {download.get("file_name")}\n'
              f'file size: {(int(download.get("file_size")) / 1024**3):.3f} GB\n'
              f'date: {download.get("date_time")}\n')
    print(f'sum size: {(sum_size / 1024**3):.3f} GB')
    print(f'sum files: {len(response)}')


def to_csv():
    rout = MAIN_URL + '/to-csv'
    response = requests.get(rout)
    print(response.status_code)


if __name__ == '__main__':
    to_csv()
