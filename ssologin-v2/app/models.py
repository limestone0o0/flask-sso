from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100))#服务器名字（数据库名称）
    user_token = db.Column(db.String(32))#服务器秘钥，默认xxmshuai
    user_address = db.Column(db.String(100))#数据库地址
