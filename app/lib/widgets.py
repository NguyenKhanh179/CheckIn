from flask import g
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget


def get_user():
    return g.user.username


class BS3TextFieldROWidget(BS3TextFieldWidget):
    def __call__(self, field, **kwargs):
        kwargs['readonly'] = 'true'
        return super(BS3TextFieldROWidget, self).__call__(field, **kwargs)


class UserLoggedWidget(BS3TextFieldWidget):
    def __call__(self, field, **kwargs):
        kwargs['readonly'] = 'true'
        kwargs['value'] = get_user()
        return super(UserLoggedWidget, self).__call__(field, **kwargs)
