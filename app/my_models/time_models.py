from flask_appbuilder import Model
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class MBTimeStatus(Model):
    __tablename__ = 'TIME_STATUS'
    status = Column(String(150), primary_key=True)
    description = Column(String(150))

    def __repr__(self):
        return self.description


class MBDimTime(Model):
    __tablename__ = 'DIM_TIME'
    dayid = Column(Date, primary_key=True)
    status = Column(String(150), ForeignKey(MBTimeStatus.status))
    trang_thai = relationship(MBTimeStatus)
    note = Column(String(2000))

    def __repr__(self):
        return self.id