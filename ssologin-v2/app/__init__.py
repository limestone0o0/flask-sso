from gevent import monkey
from flask import Flask
from flask_wtf import csrf
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

import redis

pool = redis.ConnectionPool(host='39.107.253.135', port=63790,db=12,password=7890)
r = redis.Redis(connection_pool=pool)

db = SQLAlchemy()

def create_app():
    monkey.patch_all()
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object('app.config.Develop')
    db.init_app(app)
    csrf.CSRFProtect(app)

    return app, db

