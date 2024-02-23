from datetime import datetime, timedelta
from flask import Flask, request
from config import private_config as conf
from def_db import db, User, Search, Download
import json
import csv

app = Flask(__name__)

db_uri = f"postgresql://{conf['db_user']}:{conf['db_password']}@" \
         f"{conf['db_host']}:{conf['db_port']}/{conf['db_name']}"

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db.init_app(app)

# Create the tables
with app.app_context():
    db.create_all()


def get_user_name(user_id):
    user = db.session.query(User).filter_by(user_id=user_id).first()
    if user:
        return user.user_name
    else:
        return f'no name found for {user_id}'


@app.route('/')
def main_page():
    return 'Wellcome to my goddamn data base!'


@app.route('/check-user', methods=['GET'])
def check_user():
    user_email = request.args.get('user_email')
    user_exists = len(db.session.query(User).filter_by(user_email=user_email).all()) > 0
    if user_exists:
        return '', 200
    else:
        return '', 404


@app.route('/insert-user', methods=['POST'])
def insert_user():
    data = request.get_json()
    new_user = User(user_name=data.get('user_name'), user_email=data.get('user_email'))
    user_exists = len(db.session.query(User).filter_by(user_email=new_user.user_email).all()) > 0
    if not user_exists:
        db.session.add(new_user)
        db.session.commit()
        return 'user added successfully!', 200
    return 'user already exists!', 409


@app.route('/delete-user', methods=['POST'])
def delete_user():
    data = request.get_json()
    user_exists = len(db.session.query(User).filter_by(user_email=data.get('user_email')).all()) > 0
    if user_exists:
        db.session.query(User).filter_by(user_email=data.get('user_email')).delete()
        db.session.commit()
    return f'User {data.get("user_email")} deleted!', 200


@app.route('/insert-search', methods=['POST'])
def insert_search():
    data = request.get_json()
    user_email = data.get('user_email')
    user_id = db.session.query(User).filter_by(user_email=user_email).one().user_id
    search_query = data.get('search_query')
    date_time = data.get('date_time')
    new_search = Search(user_id=user_id, search_query=search_query, date_time=date_time)
    db.session.add(new_search)
    db.session.commit()
    return '', 200


@app.route('/insert-download', methods=['POST'])
def insert_download():
    data = request.get_json()
    user_email = data.get('user_email')
    user_id = db.session.query(User).filter_by(user_email=user_email).one().user_id
    file_name = data.get('file_name')
    file_size = data.get('file_size')
    date_time = data.get('date_time')
    new_download = Download(user_id=user_id, file_name=file_name, file_size=file_size, date_time=date_time)
    db.session.add(new_download)
    db.session.commit()
    return '', 200


@app.route('/fetch-search', methods=['GET'])
def fetch_search():
    user_email = request.args.get('user_email')
    user_id = db.session.query(User).filter_by(user_email=user_email).one().user_id
    data = {search.search_id: {'search_query': search.search_query, 'date_time': str(search.date_time)}
            for search in db.session.query(Search).filter_by(user_id=user_id).all()}
    return json.dumps(data, ensure_ascii=False)


@app.route('/fetch-download', methods=['GET'])
def fetch_download():
    user_email = request.args.get('user_email')
    user_id = db.session.query(User).filter_by(user_email=user_email).one().user_id
    data = {download.download_id: {
        'file_name': download.file_name,
        'file_size': download.file_size,
        'date_time': str(download.date_time)
    }
        for download in db.session.query(Download).filter_by(user_id=user_id).all()}
    return json.dumps(data, ensure_ascii=False)


@app.route('/daily-summary', methods=['GET'])
def daily_summary():
    yesterday = datetime.utcnow() - timedelta(days=1)
    download_data = db.session.query(Download).filter(Download.date_time >= yesterday).all()
    search_data = db.session.query(Search).filter(Search.date_time >= yesterday).all()
    download_summary = {}
    for download in download_data:
        print(download)
        download_summary[download.download_id] = {'user_name': get_user_name(download.user_id),
                                                  'file_name': download.file_name,
                                                  'file_size': download.file_size,
                                                  'date': f'{download.date_time}'}
    search_summary = {}
    for search in search_data:
        search_summary[search.search_id] = {'user_name': get_user_name(search.user_id),
                                            'search_query': search.search_query,
                                            'date': f'{search.date_time}'}
    response = {
        'search_data': search_summary,
        'download_data': download_summary
    }

    return json.dumps(response, ensure_ascii=False)


@app.route('/use-summery', methods=['GET'])
def get_use_summery():
    downloads = db.session.query(Download).filter(Download.user_id != 2).all()
    searches = db.session.query(Search).all()
    downloads_size = 0
    for download in downloads:
        downloads_size += download.file_size
    use_summery = {
        'sum_searches': len(searches),
        'sum_downloads': len(downloads),
        'all_downloads_size': downloads_size / 1024**3
    }
    return json.dumps(use_summery, ensure_ascii=False)


@app.route('/user-summary/<string:username>', methods=['GET'])
def get_user_summary(username):
    user = db.session.query(User).filter_by(user_email=username).first()
    if not user:
        return {}
    user_id = user.user_id
    downloads = db.session.query(Download).filter_by(user_id=user_id).all()
    use_summary = {download.download_id: {
        'file_name': download.file_name,
        'file_size': download.file_size,
        'date_time': f'{download.date_time}'
    }
        for download in downloads
    }
    return json.dumps(use_summary, ensure_ascii=False)


@app.route('/to-csv', methods=['GET'])
def download_to_csv():
    downloads = db.session.query(Download).all()
    with open('downloads.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        data = [[get_user_name(download.user_id), download.file_name, download.file_size, download.date_time]
                for download in downloads]
        writer.writerows(data)
    return 'ok'


if __name__ == '__main__':
    app.run(port=5010)
