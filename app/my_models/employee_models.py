from flask_appbuilder import Model
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship


class MBStatus(Model):
    __tablename__ = 'mb_status'
    id = Column(Integer, primary_key=True)
    description = Column(String(500))

    def __repr__(self):
        return self.description


class MBDepartments(Model):
    __tablename__ = 'mb_departments'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(2000), unique= True)
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


class MBEmployeeStatus(Model):
    __tablename__ = "mb_employee_status"
    id = Column(Integer, primary_key=True)
    description = Column(String(200))

    def __repr__(self):
        if self.description is not None:
            return self.description
        else:
            return str(self.id)


class MBEmployee(Model):
    __tablename__ = 'mb_employee'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True)
    ho_ten = Column(String(150), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey(MBDepartments.id), nullable=False)
    ten_jira = Column(String(150))
    email = Column(String(150), nullable=False)
    ma_nv = Column(String(150))
    chucdanh = Column(String(150))
    ngayvaomb = Column(Date)
    ngaysinh = Column(Date)
    department = relationship(MBDepartments)
    STATUS = Column(Integer, ForeignKey(MBEmployeeStatus.id))
    status_desc = relationship(MBEmployeeStatus)
    note = Column(String(2000))
    def __repr__(self):
        return self.username


class MBManagers(Model):
    __tablename__ = 'mb_managers'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), ForeignKey(MBEmployee.username))
    department_id = Column(Integer, ForeignKey(MBDepartments.id))
    manager = relationship(MBEmployee)
    department = relationship(MBDepartments)

    created_date = Column(Date)
    updated_date = Column(Date)

    def __repr__(self):
        return self.username
