import os
from datetime import datetime
from flask import Flask, send_from_directory, request
from db_client import check_user, insert_search
import requests

app = Flask(__name__, static_folder='../netfree_app/build', static_url_path='/')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/search', methods=['POST'])
def search_movie():
    data = request.get_json()  # Access the data sent from React
    email = data.get('email')  # Extract the 'email' field from the data
    if not check_user(email):
        return {'user not exists': 0}
    search_string = data.get('searchText')  # Extract the 'searchString' field
    insert_search(email, search_string, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        response = requests.post('http://127.0.0.1:5001/search', data=search_string.encode('utf-8'), timeout=60)
    except requests.exceptions.ReadTimeout:
        return {}
    return response.content


@app.route('/api/download', methods=['POST'])
def download_request():
    post_request = request.json  # get the request data
    data = post_request['updateIDs']  # get the file id for download

    request_dict = {"files id": data[1:],
                    "email": data[0]}
    response = requests.post('http://127.0.0.1:5001/download', json=request_dict)
    return response.content


app.run()
