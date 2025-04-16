from flask import url_for, g
from flask_appbuilder import BaseView, expose, has_access

from app.models import api_image_model, api_log_model


class QuizView(BaseView):
    default_view = 'start'

    @expose('/index')
    @has_access
    def index(self):
        # do something with param1
        # and return to previous page or index
        self.update_redirect()
        file_name = api_image_model.get_image("GAME_START_PAGE")
        if file_name is not None:
            image_url = url_for("MBImagesView.download", filename=file_name)
            print(image_url)
        else:
            image_url = url_for('static',filename='img/start_game.png')
        return self.render_template('index.html', image_url= image_url)

    @expose('/start')
    @has_access
    def start(self):
        # do something with param1
        # and return to previous page or index
        self.update_redirect()
        return self.render_template('game.html')

    @expose('/end')
    @has_access
    def end(self):
        # do something with param1
        # and return to previous page or index
        self.update_redirect()
        username = g.user.username
        ic=-1
        logged_times = api_log_model.get_logged_in(username)
        if len(logged_times)>0:
            ic= logged_times[0]["wrong_answers"]
        # print(logged_times)
        file_name = api_image_model.get_image("GAME_END_PAGE")
        if file_name is not None:
            image_url = url_for("MBImagesView.download", filename=file_name)
            print(image_url)
        else:
            image_url=url_for('static',filename='img/end_game.jpg')
        return self.render_template('end.html', username=username, logged_times=logged_times,
                                    last_wrong_question=int(ic), image_url= image_url)