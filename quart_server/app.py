from quart import Quart, request, jsonify
from telegram_search import search_files
from get_file import GetFiles


app = Quart(__name__)


@app.route('/search', methods=['POST'])
async def search():
    data = await request.data
    query = data.decode()
    all_matches = await search_files(query, 'video')
    response = jsonify(all_matches)
    return response


@app.route('/download', methods=['POST'])
async def download():
    data = await request.get_json()
    file_ids = data['files id']
    email = data['email']
    files_handler = GetFiles(file_ids, email)
    app.add_background_task(files_handler.get_files)
    return {'status': 'אני על זה, הקבצים בקרוב אצלך'}


app.run(host='127.0.0.1', port=5001, debug=True)
