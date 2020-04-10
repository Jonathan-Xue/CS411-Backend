from server import app, sql_db

# class Course(sql_db.Model):
#     # TODO
#
#     def __repr__(self):
#         return "" # TODO

@app.route('/sql', methods=['GET'])
def sql_template():
    result = sql_db.engine.execute('SELECT id FROM test WHERE id = %s', ('Hi'))
    rows = result.fetchall()
    return rows[0]['id']
