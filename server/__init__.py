import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import spacy
nlp = None

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['CLOUD_SQL_URI']
sql_db = SQLAlchemy(app)

from . import routes