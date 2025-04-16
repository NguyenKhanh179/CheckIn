import datetime
from flask import g, request
from flask_appbuilder import ModelView, BaseView, has_access
from flask_appbuilder.api import expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms import StringField

from app.lib.widgets import BS3TextFieldROWidget, UserLoggedWidget
from app.models import api_os_daily_report_model
from app.my_models.os_models import MBOSEmployee, MBOSDepartments, MBOSManagers, MBOSCheckinDaily, MBOSReasons, MBHoliday, \
    MapOSReasonWorkTime


class MBEmployeesOSView(ModelView):
    datamodel = SQLAInterface(MBOSEmployee)

    label_columns = {'name': 'Họ tên',
                     'ten_jira': 'Jira',
                     'chucdanh': 'Chức danh', 'ngay_vao_mb': 'Ngày vào MB',
                     'ngaysinh': 'Ngày sinh', "status_desc" : "Trạng thái",'inactive_date' : 'Ngày inactive',
                     "trangthai_os" : "Trạng thái OS", "doitac": "Đối tác"}
    list_columns = ['username', 'name', 'department', 'status_desc',
                    "trangthai_os", "doitac",'ngay_vao_mb', 'inactive_date', 'note']

class MBOSDepartmentsView(ModelView):
    datamodel = SQLAInterface(MBOSDepartments)
    label_columns = {'name': 'Tên','donvi': 'Đơn vị',
                     'donvi_tt1': 'Đơn vị trực thuộc cấp 1',
                     'donvi_tt2': 'Đơn vị trực thuộc cấp 2',
                     'donvi_tt3': 'Đơn vị trực thuộc cấp 3',
                     }
    list_columns = ['name','donvi', 'donvi_tt1', 'donvi_tt2', 'donvi_tt3', 'status','level']
    related_views = [MBEmployeesOSView]

class MBOSManagersView(ModelView):
    datamodel = SQLAInterface(MBOSManagers)
    # base_filters = [
    #     ['username', FilterStartsWith,'a']
    # ]
    label_columns = {}
    list_columns = ['id', 'username','created_date', 'updated_date',
                    'manager', 'department']
    # add_columns = ['manager', 'department']
    # edit_columns = ['manager', 'department']
    #
    # # related_views = [DepartmentsView]
    #
    # show_fieldsets = [
    #     (
    #         'Info',
    #         {'fields': ['id', 'username', 'department',
    #                     'created_date', 'updated_date', 'manager', 'department']}
    #     )
    # ]


class MBOSDailyReport(BaseView):
    default_view = 'show'

    @expose('/show')
    @has_access
    def show(self):
        # do something with param1
        # and return to previous page or index
        self.update_redirect()
        # username = g.user.username
        # departments = api_daily_report_model.getDepartments()
        departments = api_os_daily_report_model.getMBOSDepartments()
        report_date_param = request.args.get("report_date")
        department_id = request.args.get("department_id")
        report_date = datetime.date.today()

        if report_date_param is not None:
            report_date = datetime.datetime.strptime(report_date_param, "%Y-%m-%d")
        report_date_str = report_date.strftime("%Y-%m-%d")
        report = []
        if department_id is not None:
            report = api_os_daily_report_model.getDailyReportByDepartment(report_date=report_date, department_id=department_id)

        return self.render_template('os_daily_report.html', department_id=department_id,
                                    report_date=report_date_str,
                                    departments=departments, report=report)

class MBOSReasonView(ModelView):
    datamodel = SQLAInterface(MBOSReasons)
    label_columns = {}
    list_columns = ['id','content','status', 'created_date','updated_date']
    show_fieldsets = [
        (
            'Info',
            {'fields': ['id','content','status', 'created_date','updated_date']}
        )
    ]
    edit_columns = [
        'id','content','status'
    ]

class MBHolidayView(ModelView):
    datamodel = SQLAInterface(MBHoliday)
    label_columns = {}
    list_columns = ['dayid','status','hs', 'note']
    show_fieldsets = [
        (
            'Info',
            {'fields': ['dayid','status','hs', 'note']}
        )
    ]
    edit_columns = [
        'dayid', 'status', 'hs', 'note'
    ]

class MapOSReasonWorkTimeView(ModelView):
    datamodel = SQLAInterface(MapOSReasonWorkTime)
    label_columns = {'reason': 'Lý do', 'status' : 'Trạng thái ghi nhân', 'hours': "Giờ"}
    list_columns = ['id','reason','status', 'hours']
    show_fieldsets = [
        (
            'Info',
            {'fields': ['id','reason','status', 'hours']}
        )
    ]
    edit_columns = [
        'id','reason','status', 'hours'
    ]

class MBOSCheckin(ModelView):
    base_permissions = ['can_edit', 'can_show']
    datamodel = SQLAInterface(MBOSCheckinDaily)
    label_columns = {"reason" : 'other reason', 'reason_str' : 'Lý do'}

    list_columns = ["username", "department", "checkin_time", "reason"]
    show_fieldsets = [
        (
            'Info',
            {'fields': ['username', 'department', 'checkin_time','checkout','note', 'transaction_date']}
        ),
        (
            'Auth',
            {'fields': ['auth_user', 'reason_str', 'auth_date']}
        )
    ]

    edit_columns = [
        'username', 'department', 'reason_str', 'auth_user',  'checkin_time','checkout','note',
    ]
    # override the 'department' field, to make it readonly on edit form
    edit_form_extra_fields = {
        'username': StringField('username', widget=BS3TextFieldROWidget()),
        'department': StringField('department', widget=BS3TextFieldROWidget()),
        'auth_user': StringField("auth_user", widget=UserLoggedWidget()),
        'checkin_time': StringField("checkin_time", widget=BS3TextFieldROWidget()),
        'checkout': StringField("checkout", widget=BS3TextFieldROWidget()),
        'note': StringField("note", widget=BS3TextFieldROWidget()),
    }

