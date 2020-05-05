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

def load_spacy_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load('en_core_web_md')

@app.route('/')
def foo():
	return "Hello World"

# TODOs
# 1. try inserting new entry with invalid primary instructor or courseNo/courseName
# 2. try inserting new course with invalid params
# 3. update only courseDesc for courses? or allow courseNo/courseName edits and cascade?

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

def normalize_score(min_s, max_s, score):
    return (score - min_s) / (max_s - min_s)

@app.route('/matches/course/<courseNo>/<courseName>', methods=['GET'])
def get_profs_for_course(courseNo, courseName):
    load_spacy_nlp()

    try:
        # 1. get course and its text data
        q = '''
            SELECT courseDesc
            FROM csCourse
            WHERE courseNo = %s AND courseName = %s;
        '''

        result = sql_db.engine.execute(q, (courseNo, courseName))
        if result is None:
            return { 'message': "Invalid query." }
        res = result.fetchone()

        courseDesc = res["courseDesc"]
        course_text = courseName + ", " + courseDesc
        course_text_nlp = nlp(course_text)

        # 2. get all instructors' research interests
        q = '''
            SELECT instructorId, instructorName, researchInterests
            FROM csInstructor;
        '''

        result = sql_db.engine.execute(q)
        if result is None:
            return { 'message': "Invalid query." }
        res = result.fetchall()

        prof_research_dict = {}
        prof_id_dict = {}
        for r in res:
            prof_research_dict[r["instructorId"]] = nlp(r["researchInterests"])
            prof_id_dict[r["instructorId"]] = r["instructorName"]

        # 3. get average GPA for instructors who have taught the course
        q = '''
            SELECT instructorId, (((SUM(aPlus) * 4) + (SUM(a) * 4) + (SUM(aMinus) * 3.67) + (SUM(bPlus) * 3.33) + (SUM(b) * 3) + (SUM(bMinus) * 2.67) + (SUM(cPlus) * 2.33) + (SUM(c) * 2) + (SUM(cMinus) * 1.67) + (SUM(dPlus) * 1.33) + (SUM(d) * 1) + (SUM(dMinus) * 0.67) + (SUM(f) * 0)) / (SUM(aPlus) + SUM(a) + SUM(aMinus) + SUM(bPlus) + SUM(b) + SUM(bMinus) + SUM(cPlus) + SUM(c) + SUM(cMinus) + SUM(dPlus) + SUM(d) + SUM(dMinus) + SUM(f))) as averageGPA
            FROM csGrade LEFT JOIN csInstructor ON csInstructor.instructorId = csGrade.primaryInstructor
            WHERE csGrade.courseNo = %s AND csGrade.courseName = %s
            GROUP BY csInstructor.instructorId;
        '''

        result = sql_db.engine.execute(q, (courseNo, courseName))
        if result is None:
            return { 'message': "Invalid query." }
        res = result.fetchall()

        prof_avg_dict = {}
        for r in res:
            prof_avg_dict[r["instructorId"]] = float(r["averageGPA"])
        base_score = float(min([r["averageGPA"] for r in res]))

        sim_score_weight = 0.1

        max_s = 0
        min_s = 0
        prof_total_scores = []
        all_scores = []

        for prof in prof_research_dict:
            sim_score = 0
            if prof_research_dict[prof].vector_norm:
                sim_score = float(course_text_nlp.similarity(prof_research_dict[prof]))

            gpa_score = base_score
            if prof in prof_avg_dict:
                gpa_score = prof_avg_dict[prof]

            total_score = sim_score * sim_score_weight + gpa_score

            prof_data = {
                "instructorId": prof,
                "instructorName": prof_id_dict[prof],
                "researchInterests": prof_research_dict[prof].text,
                "score": total_score
            }

            all_scores.append(total_score)
            prof_total_scores.append(prof_data)

        max_s = max(all_scores)
        min_s = min(all_scores)
        for prof_data in prof_total_scores:
            prof_data["score"] = normalize_score(min_s, max_s, prof_data["score"])

        sorted_prof_scores = sorted(prof_total_scores, key= lambda p : p["score"], reverse=True)
        return { "data": sorted_prof_scores[:5] }
    except Exception as e:
        return { 'message': dict(e) }

@app.route('/matches/instructor/<instructorId>', methods=['GET'])
def get_courses_for_prof(instructorId):
    load_spacy_nlp()

    try:
        # 1. get prof and his/her research interests
        q = '''
            SELECT instructorId, instructorName, researchInterests
            FROM csInstructor
            WHERE instructorId = %s;
        '''

        instructorId = 5

        result = sql_db.engine.execute(q, (instructorId,))
        if result is None:
            return { 'message': "Invalid query." }
        res = result.fetchone()

        instructorName = res["instructorName"]
        researchInterests = res["researchInterests"]

        instructor_text_nlp = nlp(researchInterests)

        if not instructor_text_nlp.vector_norm:
            return { "data": [] } # cant match prof to courses if prof research interests is empty

        # 2. get courses and their text data
        q = '''
            SELECT courseNo, courseName, courseDesc
            FROM csCourse;
        '''

        result = sql_db.engine.execute(q)
        if result is None:
            return { 'message': "Invalid query." }
        res = result.fetchall()

        course_desc_dict = {}
        for r in res:
            course_desc_dict[(r["courseNo"], r["courseName"])] = nlp(r["courseDesc"])

        course_total_scores = []
        for course in course_desc_dict:
            courseNo, courseName = course

            score = 0
            if course_desc_dict[course].vector_norm:
                score = instructor_text_nlp.similarity(course_desc_dict[course])

            course_data = {
                "courseNo": courseNo,
                "courseName": courseName,
                "courseDesc": course_desc_dict[course].text,
                "score": score
            }

            course_total_scores.append(course_data)

        sorted_course_scores = sorted(course_total_scores, key = lambda c : c["score"], reverse=True)
        return { "data": sorted_course_scores[:10] }
    except Exception as e:
        return { 'message': dict(e) }

if __name__ == '__main__':
    app.run(port=5000, debug=True)
