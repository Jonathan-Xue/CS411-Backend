import os
from flask import Flask
from flask_pymongo import pymongo

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

mongo = pymongo.MongoClient(os.environ['MONGO_URI'], maxPoolSize=50)
db = mongo.get_database('my-cluster')

from . import routes