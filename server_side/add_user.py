from postgre_db import Database

db = Database()

user_name = None
user_mail = None
while not user_mail:
    name = input('Enter the name of the user: ')
    mail = input('Enter the user mail: ')
    ok = input(f'we got the details below:\nuser name: {name}\nuser email: {mail}\nis that correct? y / n ')
    if ok.lower() == 'y':
        user_name = name
        user_mail = mail
    else:
        print('lets try again: ')

db.insert_user(user_name, user_mail)
print(f'update successfully:\nname: {user_name}\nmail: {user_mail}')
