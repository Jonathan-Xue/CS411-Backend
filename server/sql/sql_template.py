from flask import request
from server import app, sql_db

@app.route('/create-entry', methods=['POST'])
def create_entry():
    pass

@app.route('/delete-entry', methods=['DELETE'])
def delete_entry():
    pass

@app.route('/find-entries', methods=['GET'])
def find_entries():
    pass

@app.route('/create-course', methods=['POST'])
def create_course():
    pass

@app.route('/update-course', methods=['PUT'])
def update_course():
    pass

@app.route('/delete-course', methods=['DELETE'])
def delete_course():
    pass

@app.route('/find-course', methods=['GET'])
def find_course():
    pass

@app.route('/entries', methods=['GET'])
def get_all_entries():
    result = sql_db.engine.execute('SELECT * FROM csGrade')
    rows = result.fetchall()
    row_dicts = [dict(row) for row in rows]
    row_data = { 'data': row_dicts, 'length': len(row_dicts) }
    return row_data

@app.route('/courses', methods=['GET'])
def get_all_courses():
    result = sql_db.engine.execute('SELECT * FROM csCourse')
    rows = result.fetchall()
    row_dicts = [dict(row) for row in rows]
    row_data = { 'data': row_dicts, 'length': len(row_dicts) }
    return row_data

@app.route('/sql', methods=['GET'])
def sql_template():
    result = sql_db.engine.execute('SELECT id FROM test WHERE id = %s', ('Hi'))
    rows = result.fetchall()
    return rows[0]['id']
