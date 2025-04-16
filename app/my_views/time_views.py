from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.my_models.time_models import MBTimeStatus, MBDimTime


class MBTimeStatusView(ModelView):
    datamodel = SQLAInterface(MBTimeStatus)


class MBDimTimeView(ModelView):
    datamodel = SQLAInterface(MBDimTime)

    order_columns = ('dayid', 'desc')
    label_columns = {'dayid': 'Ngày', 'trang_thai': 'Trạng thái', 'note': 'Chú thích'}
    list_columns = ['dayid', 'trang_thai', 'note']
    add_columns = ['dayid', 'trang_thai', 'note']

    show_fieldsets = [
        (
            'Info',
            {'fields': ['dayid', 'trang_thai', 'note']}
        )
    ]