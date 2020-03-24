from server import app

# Note: Don't pip install specific versions
# https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
@app.route('/sql')
def sql_template():
	return ("SQL")