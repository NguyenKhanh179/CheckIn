import uuid

import flask_login
from flask import session

from app.models import api_log_model


@flask_login.user_logged_in.connect
def login(sender, user):
    # print(user, "login", user.username)
    uid = uuid.uuid4()
    session["uid"]= uid
    api_log_model.insert_access_log(user.username, "login", uid=uid)

@flask_login.user_logged_out.connect
def logout(sender, user):
    # print(user, "logout", user.username)
    uid = uuid.uuid4()
    session["uid"] = uid
    api_log_model.insert_access_log(user.username, "logout", uid=uid)
