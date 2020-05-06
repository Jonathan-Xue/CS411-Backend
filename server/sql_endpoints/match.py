from flask import request
from server import app, sql_db, nlp, spacy

def load_spacy_nlp():
    global nlp
    if nlp is None:
        if app.config['DEVELOPMENT']:
            nlp = spacy.load('en_core_web_md')
        else:
            nlp = spacy.load('en_core_web_sm')

def normalize_score(min_s, max_s, score):
    return (score - min_s) / (max_s - min_s)

@app.route('/matches/course/<courseNo>/<courseName>', methods=['GET'])
def get_profs_for_course(courseNo, courseName):
    load_spacy_nlp()

    try:
        # Course & Text Data
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

        # Instructor Research Interests
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

        # Avg GPA For Instructors Who've Taught The Course
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

        base_score = 0
        prof_avg_dict = {}
        if len(res) != 0:
            for r in res:
                prof_avg_dict[r["instructorId"]] = float(r["averageGPA"])
            base_score = float(min([r["averageGPA"] for r in res]))

        # Calculate Total Score
        prof_total_scores = []
        all_scores = []
        similarity_weight = 1.0
        gpa_weight = 0.25 # GPA Is Scaled Out Of 4.0

        for prof in prof_research_dict:
            sim_score = 0
            if prof_research_dict[prof].vector_norm:
                sim_score = float(course_text_nlp.similarity(prof_research_dict[prof]))

            gpa_score = base_score
            if prof in prof_avg_dict:
                gpa_score = prof_avg_dict[prof]

            total_score = sim_score * similarity_weight + gpa_weight * gpa_score

            prof_data = {
                "instructorId": prof,
                "instructorName": prof_id_dict[prof],
                "researchInterests": prof_research_dict[prof].text,
                "score": total_score
            }

            all_scores.append(total_score)
            prof_total_scores.append(prof_data)

        # Normalize & Top Five
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
        # Instructor Research Interests
        q = '''
            SELECT instructorId, instructorName, researchInterests, COUNT(*) AS termsTaught
            FROM csInstructor LEFT JOIN csGrade ON csInstructor.instructorId = csGrade.primaryInstructor
            WHERE instructorId = %s;
        '''

        result = sql_db.engine.execute(q, (instructorId,))
        if result is None:
            return { 'message': "Invalid query." }
        res = result.fetchone()

        instructorName = res["instructorName"]
        researchInterests = res["researchInterests"]
        termsTaught = int(res["termsTaught"])

        instructor_text_nlp = nlp(researchInterests)

        if not instructor_text_nlp.vector_norm:
            return { "data": [] }

        # Courses & Text Data
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

        # Courses Instructor Has Previously Taught
        q = '''
            SELECT courseNo, courseName, COUNT(*) AS cnt
            FROM csGrade
            WHERE primaryInstructor = %s
            GROUP BY courseNo, courseName;
        '''

        result = sql_db.engine.execute(q, (instructorId,))
        if result is None:
            return { 'message': "Invalid query." }
        res = result.fetchall()

        course_taught_dict = {}
        for r in res:
            course_taught_dict[(r["courseNo"], r["courseName"])] = r["cnt"] / termsTaught

        # Calculate Total Score
        all_scores = []
        course_total_scores = []
        similarity_weight = 1.0
        taught_weight = 1.0

        for course in course_desc_dict:
            courseNo, courseName = course

            score = 0
            if course in course_taught_dict:
                score += taught_weight * course_taught_dict[course]

            if course_desc_dict[course].vector_norm:
                score += similarity_weight * instructor_text_nlp.similarity(course_desc_dict[course])

            course_data = {
                "courseNo": courseNo,
                "courseName": courseName,
                "courseDesc": course_desc_dict[course].text,
                "score": score
            }

            all_scores.append(score)
            course_total_scores.append(course_data)

        # Normalize & Top Five
        max_s = max(all_scores)
        min_s = min(all_scores)
        for course_data in course_total_scores:
            course_data["score"] = normalize_score(min_s, max_s, course_data["score"])

        sorted_course_scores = sorted(course_total_scores, key = lambda c : c["score"], reverse=True)
        return { "data": sorted_course_scores[:10] }
    except Exception as e:
        return { 'message': dict(e) }