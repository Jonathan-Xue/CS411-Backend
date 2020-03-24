from . import app
from .nosql import nosql_template
from .sql import sql_template

@app.route('/')
def foo():
	return "Hello World"

nosql_template
sql_template