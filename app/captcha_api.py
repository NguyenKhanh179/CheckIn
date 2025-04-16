from flask_appbuilder import expose
from flask_appbuilder.api import BaseApi

from . import appbuilder

class CaptchaApi(BaseApi):

    @expose('/refresh')
    def get_question(self):
        image = self.appbuilder.captcha.generate()
        return self.response(200, response_code=0, image = image)
appbuilder.add_api(CaptchaApi)