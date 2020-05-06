from flask import request
from server import app, sql_db

@app.route('/entries', methods=['GET','POST'])
def entries():
    if request.method == 'GET':
        try:
            # Query
            query = '''
                SELECT csGrade.*, csInstructor.instructorName AS instructorName
                from csGrade LEFT JOIN csInstructor
                ON csGrade.primaryInstructor = csInstructor.instructorId;
            '''

            result = sql_db.engine.execute(query)
            if result is None:
                return { 'message': "Invalid query." }
            rows = result.fetchall()

            # Parse Output
            row_dicts = [dict(row) for row in rows]
            row_data = { 'data': row_dicts, 'length': len(row_dicts) }

            return row_data
        except Exception as e:
            return { 'message': dict(e) }

    elif request.method == 'POST':
        try:
            # Parse Arguments
            data = request.json
            create_data = (data['courseNo'], data['courseName'], data['year'], data['term'],
                           data['primaryInstructor'], data['aPlus'], data['a'], data['aMinus'],
                           data['bPlus'], data['b'], data['bMinus'], data['cPlus'], data['c'],
                           data['cMinus'], data['dPlus'], data['d'], data['dMinus'], data['f'])

            # Query
            create_query = """INSERT INTO csGrade
                       (courseNo, courseName, year, term, primaryInstructor, aPlus, a, aMinus, bPlus, b, bMinus, cPlus, c, cMinus, dPlus, d, dMinus, f)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            sql_db.engine.execute(create_query, create_data)

            return { "message": "OK" }
        except Exception as e:
            return { 'message': dict(e) }
    else:
        return { "message": "Invalid request method." }

@app.route('/entries/<courseNo>/<courseName>/<year>/<term>/<primaryInstructor>', methods=['DELETE'])
def entries_dup(courseNo, courseName, year, term, primaryInstructor):
    if request.method == 'DELETE':
        try:
            # Parse Arguments
            delete_data = (courseNo, courseName, year, term, primaryInstructor)

            # Query
            delete_query = """DELETE FROM csGrade WHERE courseNo = %s AND courseName = %s AND year = %s AND term = %s AND primaryInstructor = %s;"""
            sql_db.engine.execute(delete_query, delete_data)

            # Return
            return { "message": "OK" }
        except Exception as e:
            return { 'message': dict(e) }
    else:

        return { "message": "Invalid request method." }