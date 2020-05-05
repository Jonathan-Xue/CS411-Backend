from . import app
from .sql import sql_template

@app.route('/')
def foo():
	return "Hello World"

sql_template
