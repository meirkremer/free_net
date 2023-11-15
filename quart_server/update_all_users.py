from postgre_db import Database
from db_client import insert_user


old_db = Database()
all_users = old_db.print_users()
for user in all_users:
    status = insert_user(user[0], user[1])
    if status:
        print(f'user {user[0]} insert!')
    else:
        print(f'user {user[0]} already exist!')
