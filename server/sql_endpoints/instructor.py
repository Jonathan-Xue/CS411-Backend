from flask import request
from server import app, sql_db

@app.route('/instructors', methods=['GET', 'POST'])
def instructors():
    if request.method == 'GET':
        # Query
        result = sql_db.engine.execute("SELECT * FROM csInstructor")
        if result is None:
            return { 'message': "Invalid query." }
        rows = result.fetchall()

        # Parse Output
        row_dicts = [dict(row) for row in rows]
        row_data = { 'data': row_dicts, 'length': len(row_dicts) }

        # Return
        return row_data

    elif request.method == 'POST':
        # Parse Arguments
        data = request.json
        create_data = (data['instructorName'], data['researchInterests'])

        # Query
        create_query = """INSERT INTO csInstructor
                   (instructorName, researchInterests)
                   VALUES (%s, %s);"""
        sql_db.engine.execute(create_query, create_data)

        return { "message": "OK" }
    else:

        return { "message": "Invalid request method." }

@app.route('/instructors/<instructorId>', methods=['PUT', 'DELETE'])
def instructors_dup(instructorId):
    if request.method == 'PUT':
        # Parse Arguments
        data = request.json
        update_data = (data['researchInterests'], instructorId)

        # Query
        update_query = """UPDATE csInstructor
                       SET researchInterests = %s
                       WHERE instructorId = %s;"""
        sql_db.engine.execute(update_query, update_data)

        # Return
        return { "message": "OK" }

    elif request.method == 'DELETE':
        # Parse Arguments
        delete_data = (instructorId,)

        # Query
        delete_query = """DELETE FROM csInstructor WHERE instructorId = %s;"""
        sql_db.engine.execute(delete_query, delete_data)

        # Return
        return { "message": "OK" }
    else:

        return { "message": "Invalid request method." }