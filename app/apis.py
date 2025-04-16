#  -*- coding: utf-8 -*-
import datetime
from hashlib import md5

from flask import request, g, session
from flask_appbuilder import has_access
from flask_appbuilder.api import BaseApi, expose
from flask_login import current_user

from . import app
from .models import api_question_model
from .models import api_log_model
from .models import user_model

class QuizApi(BaseApi):

    @expose('/getQuestions')
    @has_access
    def get_question(self):
        # if current_user or not current_user.is_authenticated():
        #     return  self.response_403();
        get_question_type = app.config['GET_QUESTION_TYPE']
        print("question_type=", get_question_type)
        if get_question_type == 1:
            username = g.user.username
            user_info = user_model.get_user(username)
            print("user_info=", user_info)
            if user_info is not None and user_info['department_id'] is not None:
                department_id = user_info['department_id']
                my_questions = api_question_model.get_question_by_don_vi(department_id)
                if len(my_questions)==0:
                    my_questions = api_question_model.get_question()
            else:
                my_questions = api_question_model.get_question()
        else:
            my_questions = api_question_model.get_question()
        # print(json.dumps(my_questions))

        return self.response(200, response_code=0, max_questions=len(my_questions), pass_point=5,
                             results=my_questions)

    @expose('/insertAnswers', methods=['POST'])
    @has_access
    def insert_answers(self):
        # if current_user or not current_user.is_authenticated():
        #     return  self.response_403();
        # print(json.dumps(my_questions))
        ip = request.remote_addr
        data = request.get_json()
        correct_answer = data['correct_answer']
        wrong_answers = data['wrong_answers']
        answers = data['answers']
        questions = data['questions']
        answer_time = data['answer_time']
        # print("a", answer_time)
        # print("insert answer",data, data['correct_answer'], data['answers'], data['questions'])
        username = g.user.username
        uid = session["uid"]
        # date_insert = datetime.date.today().__str__()
        # answer_key = md5((username+questions+date_insert).encode())
        api_log_model.insert_answer(username=username, ip=ip, name=str(current_user), correct_answer=correct_answer,
                                 answers=answers, questions=questions, wrong_answers=wrong_answers,
                                    answer_time=answer_time,
                                    uid=uid)
        return self.response(200, message="Success")


