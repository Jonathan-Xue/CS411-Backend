from flask import request
from server import app, sql_db

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == 'GET':
        try:
            # Query
            result = sql_db.engine.execute('SELECT * FROM csCourse;')
            if result is None:
                return { 'message': "Invalid query." }
            rows = result.fetchall()

            # Parse Output
            row_dicts = [dict(row) for row in rows]
            row_data = { 'data': row_dicts, 'length': len(row_dicts) }

            # Return
            return row_data
        except Exception as e:
            return { 'message': dict(e) }

    elif request.method == 'POST':
        try:
            # Parse Arguments
            data = request.json
            create_data = (data['courseNo'], data['courseName'], data['courseDesc'])

            # Query
            create_query = """INSERT INTO csCourse
                       (courseNo, courseName, courseDesc)
                       VALUES (%s, %s, %s);"""
            sql_db.engine.execute(create_query, create_data)

            # Return
            return { "message": "OK" }
        except Exception as e:
            return { 'message': dict(e) }
    else:

        return { "message": "Invalid request method." }

@app.route('/courses/<courseNo>/<courseName>', methods=['PUT', 'DELETE'])
def courses_dup(courseNo, courseName):
    if request.method == 'PUT':
        try:
            # Parse Arguments
            data = request.json
            update_data = (data['courseDesc'], courseNo, courseName)

            # Query
            update_query = """UPDATE csCourse
                           SET courseDesc = %s
                           WHERE courseNo = %s AND courseName = %s;"""
            sql_db.engine.execute(update_query, update_data)

            # Return
            return { "message": "OK" }
        except Exception as e:
            return { 'message': dict(e) }

    elif request.method == 'DELETE':
        try:
            # Parse Arguments
            delete_data = (courseNo, courseName)

            # Query
            delete_query = """DELETE FROM csCourse WHERE courseNo = %s AND courseName = %s;"""
            sql_db.engine.execute(delete_query, delete_data)

            # Return
            return { "message": "OK" }
        except Exception as e:
            return { 'message': dict(e) }
    else:

        return { "message": "Invalid request method." }