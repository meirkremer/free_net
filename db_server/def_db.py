from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'all_users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    user_email = db.Column(db.String(50), unique=True)


class Search(db.Model):
    __tablename__ = 'searches'
    search_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    search_query = db.Column(db.Text)
    date_time = db.Column(db.DateTime)


class Download(db.Model):
    __tablename__ = 'download'
    download_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    file_name = db.Column(db.String(255))
    file_size = db.Column(db.BigInteger)
    date_time = db.Column(db.DateTime)
