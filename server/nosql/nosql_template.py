from flask import jsonify
from flask import request

from server import app, db

@app.route('/nosql', methods=['GET'])
def nosql_template():
	return jsonify({"nosql" : db.users.find()})