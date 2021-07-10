from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

from route import *
    
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=True)
