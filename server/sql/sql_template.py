from server import app, sql_db

# class Course(sql_db.Model):
#     # TODO
#
#     def __repr__(self):
#         return "" # TODO

# Note: Don't pip install specific versions
# https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
@app.route('/sql', methods=['GET'])
def sql_template():
    result = sql_db.session.execute('SELECT id FROM test WHERE id = :val', {'val': "Hi"})
    return result[0]
