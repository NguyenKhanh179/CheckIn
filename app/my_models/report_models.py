from sqlalchemy.orm import relationship

from app.my_models.default_models import DefaultModel
from flask_appbuilder import Model
from sqlalchemy import Column, String, Date, Integer, ForeignKey

from app.my_models.employee_models import MBEmployee


class DailyReportModels(DefaultModel):
    def getDailyReport(self, report_date):
        # --where transaction_date = to_date(':report_date','yyyyMMdd')
        query = '''
        select 
        id, username, department, created_date, transaction_date, 
        reason, auth_user, auth_date, checkin_time, checkin_time 
        from mb_checkin_daily
        where transaction_date = to_date(:report_date,'yyyyMMdd')
        '''
        report = []
        # create a Session
        session = self.get_session()
        res = None
        data = {
            "report_date": report_date.strftime("%Y%m%d")
        }
        try:
            res = session.execute(query, data)
            for r in res:
                # print(r)
                report.append({
                    "id": r["id"],
                    "username": r["username"],
                    "phong": r["department"],
                    "checkin": r["checkin_time"],
                    "reason": r["reason"] if r["reason"] is not None else '',
                    "auth_user": r["auth_user"] if r["auth_user"] is not None else ''
                })

            return report
        finally:
            if res is not None:
                res.close()

    def getDepartments(self):
        query = '''
                select id, name, created_date, updated_date 
                from mb_departments
                where status_id = 1
				and level >=2
                '''
        result = []
        # create a Session
        session = self.get_session()
        res = None
        try:
            res = session.execute(query)
            for r in res:
                # print(r)
                result.append({
                    "id": r["id"],
                    "name": r["name"]
                })
            return result
        finally:
            if res is not None:
                res.close()
        return result

    def getDepartmentsbyUsername( self,username):
        query = '''
            WITH v_admin AS (
                SELECT r.`user_id`, u.`username`
                FROM `ab_user_role` r, `ab_user` u
                WHERE r.`role_id` IN
                (
                SELECT id
                FROM `ab_role`
                WHERE NAME='Admin'
                )
                AND r.`user_id` = u.`id`
            ),
            v_departments AS (
                SELECT * FROM mb_departments
                WHERE #status_id = 1 AND 
                LEVEL >=2
            ),
            v_d_admin AS (
                SELECT t1.id department_id
                FROM v_departments t1, v_admin t2
                WHERE t2.`username`= :username
            ),
            v_manager AS (
                SELECT department_id
                FROM mb_managers
                WHERE username=:username
            )
            SELECT id,name
            FROM 
            (
                SELECT *
                FROM v_manager
                UNION ALL
                SELECT *
                FROM v_d_admin
            ) d1, v_departments d2
            WHERE d1.department_id = d2.id
                '''
        result = []
        # create a Session
        session = self.get_session()
        data = {
            "username": username
        }
        res = None
        try:
            res = session.execute(query,data)
            for r in res:
                print(r)
                result.append({
                    "id": r[0],
                    "name": r[1]
                })
            return result
        finally:
            if res is not None:
                res.close()
        return result

    def getDailyReportByDepartment(self, report_date, department_id):
        # --where transaction_date = to_date(':report_date','yyyyMMdd')
        query = '''
        SELECT 
            t1.id, t1.username, t1.department, t1.created_date, t1.transaction_date, 
            '' reason, t1.auth_user, t1.auth_date, t1.checkin_time
        FROM mb_checkin_daily t1
        where transaction_date = str_to_date(:report_date,'%Y%m%d')
        '''
        report = []
        # create a Session
        session = self.get_session()
        res = None
        data = {
            "report_date": report_date.strftime("%Y%m%d")
        }
        try:
            res = session.execute(query, data)
            for r in res:
                # print(r)
                report.append({
                    "id": r["id"],
                    "username": r["username"],
                    "phong": r["department"],
                    "checkin": r["checkin_time"],
                    "reason": r["reason"] if r["reason"] is not None else '',
                    "auth_user": r["auth_user"] if r["auth_user"] is not None else ''
                })

            return report
        finally:
            if res is not None:
                res.close()

    def getDailyReportByDepartmentInTime(self, from_date, to_date, department_id):
        # --where transaction_date = to_date(':report_date','yyyyMMdd')
        query = '''
        SELECT 
            t1.id, t1.username, t1.department, t1.created_date, t1.transaction_date, 
            '' reason, t1.auth_user, t1.auth_date, t1.checkin_time
        FROM mb_checkin_daily t1
        where transaction_date between str_to_date(:from_date,'%Y%m%d') and str_to_date(:to_date,'%Y%m%d')
        '''
        report = []
        # create a Session
        session = self.get_session()
        res = None
        data = {
            "from_date": from_date.strftime("%Y%m%d"),
            "to_date": to_date.strftime("%Y%m%d")
        }
        try:
            res = session.execute(query, data)
            for r in res:
                # print(r)
                report.append({
                    "transaction_date": r["transaction_date"],
                    "id": r["id"],
                    "username": r["username"],
                    "phong": r["department"],
                    "checkin": r["checkin_time"],
                    "reason": r["reason"] if r["reason"] is not None else '',
                    "auth_user": r["auth_user"] if r["auth_user"] is not None else ''
                })

            return report
        finally:
            if res is not None:
                res.close()

class MBReasons(Model):
    __tablename__ = 'mb_reasons'
    id = Column(Integer, primary_key=True)
    content = Column(String(2000))
    created_date = Column(Date)
    updated_date = Column(Date)
    status = Column(Integer, default=1)

    def __repr__(self):
        return self.content

class MBCheckinDaily(Model):
    __tablename__ = 'mb_checkin_daily'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), ForeignKey(MBEmployee.username))
    department = Column(String(150))
    checkin_time = Column(Date)
    created_date = Column(Date)
    transaction_date = Column(Date)
    reason = Column(String(150))
    reason_id = Column(Integer, ForeignKey(MBReasons.id))
    reason_str = relationship(MBReasons)
    auth_user = Column(String(150))
    auth_date = Column(Date)

    def __repr__(self):
        return self.id

