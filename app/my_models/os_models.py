from flask_appbuilder import Model
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.my_models.default_models import DefaultModel
from app.my_models.employee_models import MBEmployeeStatus, MBStatus, MBEmployee

class MBOSReasons(Model):
    __tablename__ = 'mb_os_reasons'
    id = Column(Integer, primary_key=True)
    content = Column(String(2000))
    created_date = Column(Date)
    updated_date = Column(Date)
    status = Column(Integer, default=1)

    def __repr__(self):
        return self.content
class MBHoliday(Model):
    __tablename__ = 'mb_holiday'
    dayid = Column(Date, primary_key=True)
    status = Column(String(2000))
    note = Column(String(2000))
    hs = Column(Integer)
    def __repr__(self):
        return self.dayid

class MapOSReasonWorkTime(Model):
    __tablename__ = 'map_os_reason_work_time'
    id = Column(Integer, primary_key=True)
    reason_id = Column(Integer, ForeignKey(MBOSReasons.id))
    reason = relationship(MBOSReasons)
    status = Column(String(2000))
    hours = Column(Integer)
    def __repr__(self):
        return self.STATUS

class MBOSDepartments(Model):
    __tablename__ = 'mb_os_departments'
    id = Column(Integer, primary_key=True)
    name = Column(String(2000))
    created_date = Column(Date)
    updated_date = Column(Date)
    donvi = Column(String(500))
    donvi_tt1 = Column(String(500))
    donvi_tt2 = Column(String(500))
    donvi_tt3 = Column(String(500))
    level = Column(Integer)
    status_id = Column(Integer, ForeignKey(MBStatus.id))
    status = relationship(MBStatus)

    def __repr__(self):
        return self.name

class MBOSEmployee(Model):
    __tablename__ = 'MB_OS_EMPLOYEE'
    id = Column(Integer, primary_key= True)
    username = Column(String(150), unique=True, nullable=False)
    name = Column(String(150), unique=True, nullable=False)
    department_id = Column(Integer,ForeignKey(MBOSDepartments.id),  nullable=False)
    email = Column(String(150), nullable=False)
    department = relationship(MBOSDepartments)
    STATUS_id = Column(Integer, ForeignKey(MBEmployeeStatus.id))
    status_desc = relationship(MBEmployeeStatus)
    ngay_vao_mb = Column(Date)
    inactive_date= Column(Date)
    ma_os = Column(String(2000))
    doitac = Column(String(2000))
    loaihinh = Column(String(2000))
    trangthai_os = Column(String(2000))
    note = Column(String(2000))

    def __repr__(self):
        return self.username

class MBOSManagers(Model):
    __tablename__ = 'mb_os_managers'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), ForeignKey(MBEmployee.username))
    department_id = Column(Integer, ForeignKey(MBOSDepartments.id))
    manager = relationship(MBEmployee)
    department = relationship(MBOSDepartments)

    created_date = Column(Date)
    updated_date = Column(Date)

    def __repr__(self):
        return self.username


class MBOSDailyReportModels(DefaultModel):
    def getDailyReport(self, report_date):
        # --where transaction_date = to_date(':report_date','yyyyMMdd')
        query = '''
        select 
        id, username, department, created_date, transaction_date, 
        reason, auth_user, auth_date, checkin_time, checkin_time,
        t1.checkin, t1.checkout, t1.note
        from mb_os_checkin_daily t1
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
                    "checkin": r["checkin"],
                    "checkout": r["checkout"],
                    "note" : r["note"],
                    "reason": r["reason"] if r["reason"] is not None else '',
                    "auth_user": r["auth_user"] if r["auth_user"] is not None else ''
                })

            return report
        finally:
            if res is not None:
                res.close()

    def getMBOSDepartments(self):
        query = '''
                select id, name, created_date, updated_date 
                from mb_os_departments
                where status_id = 1
                and level =2
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

    def getDailyReportByDepartment(self, report_date, department_id):
        # --where transaction_date = to_date(':report_date','yyyyMMdd')
        query = '''
        SELECT 
            t1.id, t1.username, t1.department, t1.created_date, t1.transaction_date, 
            nvl(t2.content,t1.reason) reason, t1.auth_user, t1.auth_date, t1.checkin_time,
            t1.checkin, t1.checkout, t1.note            
        FROM mb_os_checkin_daily t1
        LEFT JOIN mb_os_reasons t2
        ON t1.reason_id = t2.id
        where transaction_date = str_to_date(:report_date,'%Y%m%d')
        and department_id= :department
        '''
        report = []
        # create a Session
        session = self.get_session()
        res = None
        data = {
            "report_date": report_date.strftime("%Y%m%d"),
            "department": department_id
        }
        try:
            res = session.execute(query, data)
            for r in res:
                # print(r)
                report.append({
                    "id": r["id"],
                    "username": r["username"],
                    "phong": r["department"],
                    "checkin": r["checkin"],
                    "checkout": r["checkout"],
                    "note" : r["note"],
                    "reason": r["reason"] if r["reason"] is not None else '',
                    "auth_user": r["auth_user"] if r["auth_user"] is not None else ''
                })

            return report
        finally:
            if res is not None:
                res.close()

class MBOSCheckinDaily(Model):
    __tablename__ = 'mb_os_checkin_daily'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), ForeignKey(MBOSEmployee.username))
    department = Column(String(150))
    checkin_time = Column(Date)
    created_date = Column(Date)
    transaction_date = Column(Date)
    reason = Column(String(150))
    reason_id = Column(Integer, ForeignKey(MBOSReasons.id))
    reason_str = relationship(MBOSReasons)
    auth_user = Column(String(150))
    auth_date = Column(Date)
    checkin = Column(Date)
    checkout = Column(Date)
    note = Column(String(4000))

    def __repr__(self):
        return self.id