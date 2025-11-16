import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder="../templates",static_folder="../static")

if os.getenv("PRODUCTION") == "True":
    connection_string = (
        f'mysql+mysqldb://{os.getenv("MYSQL_USER")}:'
        f'{os.getenv("MYSQL_PASSWORD")}@'
        f'{os.getenv("MYSQL_HOST")}/'
        f'{os.getenv("MYSQL_DATABASE")}'
    )
else:
    connection_string = 'mysql+mysqldb://root:123456@localhost/news_app_db'

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended to suppress warnings
db = SQLAlchemy()
db.init_app(app)
