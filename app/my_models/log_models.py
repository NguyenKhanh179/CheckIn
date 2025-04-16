from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Date

from app.my_models.default_models import DefaultModel


class AnswerLogModel(Model):
    __tablename__ = 'answer_logs'
    id = Column(Integer, primary_key=True)
    username = Column(String(500))
    name = Column(String(500))
    ip = Column(String(50))
    correct_answer = Column(Integer)
    answers = Column(String(2000))
    questions = Column(String(2000))
    created_time = Column(Date)
    logged_time = Column(Date)
    logged_date = Column(Date)

    def __repr__(self):
        return self.name


class APILogModel(DefaultModel):

    def insert_access_log(self, username, action,uid=None):
        row = {
            "username": username,
            "action": action,
            "uid" : uid
        }

        query = '''
                insert into access_logs(username,action, transaction_date, uid)
                values
                (:username,:action, current_date,:uid)
                '''
        res = None
        session = self.get_session()
        try:
            session.execute(query, row)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def insert_answer(self, username, name, ip, correct_answer=0, wrong_answers=None,
                      answers=None, questions=None, answer_time=-1, uid=None):
        row = {
            "username": username,
            "name": name,
            "ip": ip,
            "correct_answer": correct_answer,
            "answers": answers,
            "questions": questions,
            "wrong_answers": wrong_answers,
            "answer_time": answer_time,
            "uid" : uid
        }

        query = '''
        insert into answer_logs(username,name, ip, correct_answer, answers, 
        questions,wrong_answers, answer_time, uid)
        values
        (:username,:name,:ip,:correct_answer,:answers,:questions, :wrong_answers, :answer_time, :uid)
        '''
        res = None
        session = self.get_session()
        try:
            session.execute(query, row)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def get_logged_in(self, username, date=None):
        session = self.get_session()
        data = {
            "username": username,
            "date": date
        }
        if date is None:
            query = '''
            SELECT 
            ROW_NUMBER() OVER() id,t1.ip,t1.logged_time, 
            t1.wrong_answers, t1.answer_time, t1.uid,
            t2.`created_date` login_time
            FROM answer_logs t1
            LEFT JOIN access_logs t2
            ON t1.username = t2.`username`
            AND t1.uid= t2.uid
            AND t1.logged_date = t2.`transaction_date`
            AND t1.username = :username
            AND t1.`logged_date` = DATE(SYSDATE())
            AND t2.`transaction_date` = DATE(SYSDATE())
            WHERE t1.username= :username
            AND `logged_date` = DATE(SYSDATE())
            ORDER BY logged_time
            '''

        else:
            query = '''
            SELECT 
            ROW_NUMBER() OVER() id,t1.ip,t1.logged_time, 
            t1.wrong_answers, t1.answer_time, t1.uid,
            t2.`created_date` login_time
            FROM answer_logs t1
            LEFT JOIN access_logs t2
            ON t1.username = t2.`username`
            AND t1.uid= t2.uid
            AND t1.logged_date = t2.`transaction_date`
            AND t1.username = :username
            AND t1.`logged_date` = str_to_date(':date','%Y%m%d')
            AND t2.`transaction_date` = str_to_date(':date','%Y%m%d')
            WHERE t1.username= :username
            AND `logged_date` = str_to_date(':date','%Y%m%d')
            ORDER BY logged_time
            '''
        res = None
        rs = []
        try:
            res = session.execute(query, data)
            for r in res:
                rs.append({
                    "id": r["id"],
                    "ip": r["ip"],
                    "logged_time": r["logged_time"].__str__(),
                    "wrong_answers": r["wrong_answers"],
                    "answer_time": r["answer_time"],
                    "login_time" : r["login_time"],
                })
            return rs
        except Exception:
            raise
        finally:
            if res is not None:
                res.close()