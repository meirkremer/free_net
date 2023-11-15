import psycopg2
import datetime
from config import private_config


class Database:
    def __init__(self):
        self._conn = psycopg2.connect(
            user=private_config['db_user'],
            password=private_config['db_password'],
            host=private_config['db_host'],
            port=private_config['db_port'],
            database=private_config['db_name']
        )
        self._cursor = self._conn.cursor()
        create_all_users_query = 'CREATE TABLE IF NOT EXISTS all_users (' \
                                 'name TEXT,' \
                                 'mail TEXT UNIQUE)'
        self._cursor.execute(create_all_users_query)
        self._cursor.execute('SELECT mail FROM all_users')
        for user in self._cursor.fetchall():
            email_base_host = user[0].split('@')
            search_table_name = ('search_' + email_base_host[0] + '_' + email_base_host[-1]).replace('.', '$')
            create_search_user_table_query = f'CREATE TABLE IF NOT EXISTS {search_table_name} (' \
                                             f'query TEXT,' \
                                             f'time TIMESTAMP)'
            self._cursor.execute(create_search_user_table_query)
            download_table_name = ('download_' + email_base_host[0] + '_' + email_base_host[-1]).replace('.', '$')
            create_download_user_table_query = f'CREATE TABLE IF NOT EXISTS {download_table_name} (' \
                                               f'file_name TEXT,' \
                                               f'size INTEGER,' \
                                               f'time TIMESTAMP)'
            self._cursor.execute(create_download_user_table_query)
        self._conn.commit()

    def insert_search(self, user_mail, search_query, search_datetime):
        email_base_host = user_mail.split('@')
        table_name = ('search_' + email_base_host[0] + '_' + email_base_host[-1]).replace('.', '$')
        insert_query = f'INSERT INTO {table_name} (query, time) VALUES (%s, %s)'
        self._cursor.execute(insert_query, (search_query, search_datetime))
        self._conn.commit()

    def insert_download(self, user_mail, file_name, file_size, download_datetime):
        email_base_host = user_mail.split('@')
        table_name = ('download_' + email_base_host[0] + '_' + email_base_host[-1]).replace('.', '$')
        insert_query = f'INSERT INTO {table_name} (file_name, size, time) VALUES (%s, %s, %s)'
        self._cursor.execute(insert_query, (file_name, file_size, download_datetime))
        self._conn.commit()

    def check_day_download(self, user_download_table):
        start_day = datetime.datetime.now() - datetime.timedelta(hours=24)
        size_query = f'SELECT SUM(size) FROM {user_download_table} WHERE time >= %s'
        self._cursor.execute(size_query, (start_day,))
        download_size = self._cursor.fetchone()[0]
        return download_size

    def insert_user(self, user_name, user_mail):
        insert_query = 'INSERT INTO all_users (name, mail) VALUES (%s, %s) ON CONFLICT DO NOTHING'
        self._cursor.execute(insert_query, (user_name, user_mail))
        self._conn.commit()

    def check_user(self, user_mail):
        self._cursor.execute('SELECT mail FROM all_users')
        exists_users = [u[0].lower() for u in self._cursor.fetchall()]
        if user_mail.lower() in exists_users:
            return True
        else:
            return False

    def remove_user(self, user_mail):
        delete_query = 'DELETE FROM all_users WHERE mail = %s'
        self._cursor.execute(delete_query, (user_mail,))
        self._conn.commit()


if __name__ == '__main__':
    db = Database()
    db.insert_user('meir kremer', 'marworm1@gmail.com')
    db = Database()
    db.remove_user('marworm1@gil.com')
    print(db.check_user('marworm1@gmail.com'))
    print(db.check_user('marworm'))
    test_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.insert_search('marworm1@gmail.com', 'test system', test_datetime)
    db.insert_download('marworm1@gmail.com', 'test.mkv', 14589636, test_datetime)
    download_size_day = db.check_day_download('download_marworm1_gmail$com')
    print(download_size_day)
