import os
from flask import Flask
from flask_pymongo import pymongo

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

client = pymongo.MongoClient(os.environ['MONGO_URI'])
db = client.mycluster

from . import routes