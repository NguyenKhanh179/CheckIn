import logging
from datetime import timedelta

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_login import login_manager
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha
from .index import MyIndexView

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
#app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_TYPE'] = 'redis'
import redis
app.config['SESSION_REDIS'] = redis.from_url('redis://10.1.38.109:6379')
db = SQLA(app)
Session(app)
captcha = FlaskSessionCaptcha(app)
appbuilder: AppBuilder = AppBuilder(app, db.session, indexview= MyIndexView)
appbuilder.session.permanent = True
app.permanent_session_lifetime = timedelta(minutes=15)
appbuilder.captcha = captcha
"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views
from . import captcha_api
from . import listener
