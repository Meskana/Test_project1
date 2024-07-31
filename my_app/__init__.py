from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)

app.config['SECRET_KEY'] = 'c27ef6e5e04d1cd776b5d37f97086b2b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Mail configuration

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mclaret797@gmail.com'
app.config['MAIL_PASSWORD'] = 'avhe twqt pbgf mnck'
mail = Mail(app)

from my_app import route
