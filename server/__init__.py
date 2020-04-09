import os
from flask import Flask
from flask_pymongo import pymongo
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['CLOUD_SQL_URI']
sql_db = SQLAlchemy(app)

client = pymongo.MongoClient(os.environ['MONGO_URI'])
nosql_db = client.mycluster

from . import routes
