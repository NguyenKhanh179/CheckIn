from datetime import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, String, Date, Integer, ForeignKey, text, DateTime
from sqlalchemy.orm import relationship

from app.my_models.default_models import DefaultModel
from app.my_models.employee_models import MBStatus, MBDepartments


class MBCategory(Model):
    __tablename__ = 'mb_category'
    category_id = Column(String(150), primary_key=True)
    name = Column(String(150), nullable=False)
    created_date = Column(Date)
    updated_date = Column(Date)

    def __repr__(self):
        return self.name


class MBQuestions(Model):
    __tablename__ = 'mb_questions'
    id = Column(Integer, primary_key=True)
    category = Column(String(150), ForeignKey(MBCategory.category_id))
    type = Column(String(150), nullable=False)
    difficulty = Column(String(150))
    content = Column(String(2000))
    answer1 = Column(String(2000))
    answer2 = Column(String(2000))
    answer3 = Column(String(2000))
    answer4 = Column(String(2000))
    correct_answer = Column(String(150))
    created_date = Column(Date)
    updated_date = Column(Date)
    category_content = relationship(MBCategory)

    def __repr__(self):
        return self.name


class MBCategoryConfig(Model):
    __tablename__ = 'mb_question_config'
    id = Column(Integer, primary_key=True)
    category = Column(String(150), ForeignKey(MBCategory.category_id))
    questions = Column(Integer, nullable=False)
    is_active = Column(Integer, ForeignKey(MBStatus.id))
    status = relationship(MBStatus)
    created_date = Column(Date)
    updated_date = Column(Date)
    category_content = relationship(MBCategory)

    def __repr__(self):
        return self.id


class MBGroupQuestions(Model):
    __tablename__ = 'mb_group_question'
    id = Column(Integer, primary_key=True)
    description = Column(String(500))
    created_date = Column(DateTime, default=datetime.now())
    status = Column(Integer, ForeignKey(MBStatus.id), default=1)
    status_desc = relationship(MBStatus)

    def __repr__(self):
        return self.description


class GroupQuestionConfig(Model):
    __tablename__ = 'group_question_config'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey(MBGroupQuestions.id))
    group_question = relationship(MBGroupQuestions)
    category_id = Column(String(200), ForeignKey(MBCategory.category_id))
    category = relationship(MBCategory)
    count_questions = Column(Integer, default=0)
    status_id = Column(Integer, ForeignKey(MBStatus.id), default=1)
    status = relationship(MBStatus)


class MapGroupQuestionDepartment(Model):
    __tablename__ = 'map_group_question_department'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey(MBGroupQuestions.id))
    group_question = relationship(MBGroupQuestions)
    department_id = Column(Integer, ForeignKey(MBDepartments.id))
    department = relationship(MBDepartments)
    status_id = Column(Integer, ForeignKey(MBStatus.id), default=1)
    status = relationship(MBStatus)
    created_date = Column(DateTime)
    updated_date = Column(DateTime)


class ApiQuestionModel(DefaultModel):
    def get_question(self):
        print("run get random question")
        questions = []
        query = '''
        WITH 
        v_questions AS (
            SELECT *
            FROM (
                SELECT c1.*
                FROM mb_questions c1
                ORDER BY RAND()
            ) a
            limit 5
        )
        SELECT 
                id question_id, 
                category, type, difficulty, 
                content question,
                answer1,answer2, answer3,answer4, correct_answer
        FROM v_questions t
        '''
        # create a Session
        session = self.get_session()
        res = None
        try:
            res = session.execute(text(query).execution_options(autocommit=True))
            result = self.load_questions(questions, res)
            return result
        finally:
            if res is not None:
                res.close()
            # session.close()

    def get_question_by_don_vi(self, department_id):
        print("run get question by p=", department_id)
        data = {
            "department_id": department_id,
        }
        questions = []
        query = '''
        WITH v_q_config AS (
            SELECT t1.group_id, t2.description, t3.category_id category, count_questions
            FROM `map_group_question_department` t1
            ,`mb_group_question` t2, `group_question_config` t3
            WHERE t1.status_id=1
            AND t2.status=1
            AND t3.status_id =1
            AND t1.group_id = t2.id
            AND t1.group_id = t3.group_id
            and t1.department_id = :department_id
        ),
        v_questions AS (
            SELECT *
            FROM (
            SELECT c1.*, c2.count_questions,ROW_NUMBER() OVER (PARTITION BY c1.category ORDER BY RAND()) rank1
            FROM mb_questions c1, v_q_config c2
            WHERE c1.category= c2.category
            ) a
            WHERE rank1<= count_questions
        )
        SELECT 
                id question_id, 
                category, type, difficulty, 
                content question,
                answer1,answer2, answer3,answer4, correct_answer
        FROM v_questions t
        '''
        # create a Session
        session = self.get_session()
        res = None
        try:
            res = session.execute(query, data)
            result = self.load_questions(questions, res)
            return result
        finally:
            if res is not None:
                res.close()

    def load_questions(self, questions, res):
        for r in res:
            # print(r)
            type = r['type']
            question = None
            if type is not None:
                type = str(type).lower()
                if type == 'single choice':
                    question = self.get_question_info_single(r)
                elif type == 'multi choice':
                    question = self.get_question_info_multi(r)

            # print(correct_answer, correct_answer_id)
            if question is not None:
                questions.append(question)
        result = [i for i in questions if i]
        return result

    def get_question_info_single(self, r):
        correct_answer_id = r["correct_answer"]
        correct_answer = None
        incorrect_answers = [r['answer2'], r['answer1'], r['answer3'], r['answer4']]
        correct_answer = self.get_correct_question_by_id(correct_answer, correct_answer_id, r)

        if correct_answer is not None:
            incorrect_answers.remove(correct_answer)
        question = {
            "question_id": r["question_id"],
            "category": r["category"],
            "type": r["type"],
            "difficulty": r["difficulty"],
            "question": r["question"],
            "correct_answer": correct_answer,
            "incorrect_answers": incorrect_answers
        }
        return question

    def get_correct_question_by_id(self, correct_answer, correct_answer_id, r):
        if correct_answer_id == '1':
            correct_answer = r['answer1']
        elif correct_answer_id == '2':
            correct_answer = r['answer2']
        elif correct_answer_id == '3':
            correct_answer = r['answer3']
        elif correct_answer_id == '4':
            correct_answer = r['answer4']
        return correct_answer

    def get_question_info_multi(self, r):
        correct_answer_ids: str = str(r["correct_answer"])
        incorrect_answers = [r['answer2'], r['answer1'], r['answer3'], r['answer4']]
        correct_answer_ids = correct_answer_ids.strip()
        correct_ids = correct_answer_ids.split(",")
        correct_answers = []
        if len(correct_answer_ids) > 0:
            for correct_answer_id in correct_answer_ids:
                correct_answer = None
                correct_answer = self.get_correct_question_by_id(correct_answer, correct_answer_id, r)
                if correct_answer is not None:
                    correct_answers.append(correct_answer)
                    incorrect_answers.remove(correct_answer)
        question = {
            "question_id": r["question_id"],
            "category": r["category"],
            "type": r["type"],
            "difficulty": r["difficulty"],
            "question": r["question"],
            "correct_answer": correct_answers,
            "incorrect_answers": incorrect_answers
        }
        return question
