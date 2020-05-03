from flask import request
from server import app, sql_db

@app.route('/entries', methods=['GET','POST'])
def entries():
    if request.method == 'GET':
        # Query
        query = '''
            SELECT csGrade.*, csInstructor.instructorName AS instructorName
            from csGrade LEFT JOIN csInstructor
            ON csGrade.primaryInstructor = csInstructor.instructorId;
        '''

        result = sql_db.engine.execute(query)
        rows = result.fetchall()

        # Parse Output
        row_dicts = [dict(row) for row in rows]
        row_data = { 'data': row_dicts, 'length': len(row_dicts) }

        # Return
        return row_data
    elif request.method == 'POST':
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

        # Return
        return {}
    else:
        print("Error")
        return {}

@app.route('/entries/<courseNo>/<courseName>/<year>/<term>/<primaryInstructor>', methods=['PUT', 'DELETE'])
def entries_dup(courseNo, courseName, year, term, primaryInstructor):
    if request.method == 'PUT':
        # Return
        return {}
    elif request.method == 'DELETE':
        # Parse Arguments
        delete_data = (courseNo, courseName, year, term, primaryInstructor)

        # Query
        delete_query = """DELETE FROM csGrade WHERE courseNo = %s AND courseName = %s AND year = %s AND term = %s AND primaryInstructor = %s;"""
        sql_db.engine.execute(delete_query, delete_data)

        # Return
        return {}
    else:
        print("Error")
        return {}

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == 'GET':
        # Query
        result = sql_db.engine.execute('SELECT * FROM csCourse')
        rows = result.fetchall()

        # Parse Output
        row_dicts = [dict(row) for row in rows]
        row_data = { 'data': row_dicts, 'length': len(row_dicts) }

        # Return
        return row_data
    elif request.method == 'POST':
        # Parse Arguments
        data = request.json
        create_data = (data['courseNo'], data['courseName'], data['courseDesc'])

        # Query
        create_query = """INSERT INTO csCourse
                   (courseNo, courseName, courseDesc)
                   VALUES (%s, %s, %s);"""
        sql_db.engine.execute(create_query, create_data)

        # Return
        return {}
    else:
        print("Error")
        return {}

@app.route('/courses/<courseNo>/<courseName>', methods=['PUT', 'DELETE'])
def courses_dup(courseNo, courseName):
    if request.method == 'PUT':
        # Parse Arguments
        data = request.json
        update_data = (data['courseDesc'], courseNo, courseName)

        # Query
        update_query = """UPDATE csCourse
                       SET courseDesc = %s
                       WHERE courseNo = %s AND courseName = %s;"""
        sql_db.engine.execute(update_query, update_data)

        # Return
        return {}
    elif request.method == 'DELETE':
        # Parse Arguments
        delete_data = (courseNo, courseName)

        # Query
        delete_query = """DELETE FROM csCourse WHERE courseNo = %s AND courseName = %s;"""
        sql_db.engine.execute(delete_query, delete_data)

        # Return
        return {}
    else:
        print("Error")
        return {}
