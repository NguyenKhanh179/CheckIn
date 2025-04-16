import datetime

from flask import request, g
from flask_appbuilder import ModelView, BaseView, expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms import StringField

from app.lib.widgets import BS3TextFieldROWidget, UserLoggedWidget
from app.models import api_daily_report_model
from app.my_models.log_models import AnswerLogModel
from app.my_models.report_models import MBCheckinDaily, MBReasons
from flask_appbuilder.models.sqla.filters import FilterEqualFunction

class AnswerLog(ModelView):
    datamodel = SQLAInterface(AnswerLogModel)
    label_columns = {}
    base_permissions = ['can_list', 'can_show']
    list_columns = ['id', 'username', 'ip', 'logged_time', 'created_time', 'logged_date']

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['id', 'username', 'ip', 'logged_time', 'created_time', 'logged_date']}
        ),
        (
            'Detail',
            {'fields': ['correct_answer', 'answers', 'questions']}
        ),
    ]

def get_active_status():
    return "1"
class DailyReport(BaseView):
    default_view = 'show'

    @expose('/show')
    @has_access
    def show(self):
        # do something with param1
        # and return to previous page or index
        self.update_redirect()
        username = g.user.username
        # departments = api_daily_report_model.getDepartments()
        departments = api_daily_report_model.getDepartmentsbyUsername(username)
        from_date_param = request.args.get("from_date")
        to_date_param = request.args.get("to_date")
        department_id = request.args.get("department_id")
        from_date = datetime.date.today()
        to_date = datetime.date.today()

        if from_date_param is not None:
            try:
                from_date = datetime.datetime.strptime(from_date_param, "%Y-%m-%d")
            except:
                print("error in try process from date ", from_date_param)
        if to_date_param is not None:
            try:
                to_date = datetime.datetime.strptime(to_date_param, "%Y-%m-%d")
            except:
                print("error in try process to date ", to_date_param)
        from_date_str = from_date.strftime("%Y-%m-%d")
        to_date_str = to_date.strftime("%Y-%m-%d")
        report = []
        if department_id is not None:
            report = api_daily_report_model.getDailyReportByDepartmentInTime(from_date=from_date,
                                                                             to_date=to_date,
                                                                             department_id=department_id)

        return self.render_template('daily_report.html', department_id=department_id,
                                    from_date=from_date_str,
                                    to_date=to_date_str,
                                    departments=departments, report=report)

class MBCheckin(ModelView):
    base_permissions = ['can_edit', 'can_show']
    datamodel = SQLAInterface(MBCheckinDaily)
    label_columns = {"reason" : 'Lý do khác', 'reason_str' : 'Lý do'}

    list_columns = ["username", "department", "checkin_time", "reason_str"]
    show_fieldsets = [
        (
            'Info',
            {'fields': ['username', 'department', 'checkin_time', 'transaction_date']}
        ),
        (
            'Auth',
            {'fields': ['auth_user', 'reason_str','reason', 'auth_date']}
        )
    ]

    edit_columns = [
        'username', 'department', 'reason_str', 'auth_user'
    ]
    # override the 'department' field, to make it readonly on edit form
    edit_form_extra_fields = {
        'username': StringField('username', widget=BS3TextFieldROWidget()),
        'department': StringField('department', widget=BS3TextFieldROWidget()),
        'auth_user': StringField("auth_user", widget=UserLoggedWidget())
    }
    edit_form_query_rel_fields = {'reason_str': [['status', FilterEqualFunction, get_active_status]]}

class MBReasonView(ModelView):
    datamodel = SQLAInterface(MBReasons)
    base_permissions = ['can_list', 'can_show', 'can_edit','can_add']
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