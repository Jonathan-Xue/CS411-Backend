from flask import jsonify
from flask import request
from bson import json_util

from server import app, nosql_db

@app.route('/nosql', methods=['GET'])
def nosql_template():
	output = json_util.dumps(nosql_db.users.find())
	return jsonify({"nosql": output})
