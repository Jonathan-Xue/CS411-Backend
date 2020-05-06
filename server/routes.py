from . import app
from .sql_endpoints import course
from .sql_endpoints import entry
from server.sql_endpoints import instructor
from server.sql_endpoints import match

@app.route('/')
def foo():
	return "Hello World"