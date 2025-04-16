#  -*- coding: utf-8 -*-
import os

from flask import render_template, g, send_from_directory

from . import appbuilder, db, app
from .apis import QuizApi

# create my_models
from .my_views.employee_views import EmployeesView, DepartmentsView, ManagersView
from .my_views.os_views import MBEmployeesOSView, MBOSDepartmentsView, MBOSManagersView, MBOSDailyReport, MBOSCheckin, \
    MBOSReasonView, MBHolidayView, MapOSReasonWorkTimeView
from .my_views.page_config_views import MBImagesView, PageTypeView, PageConfigView
from .my_views.question_config_views import MBQuestionsView, MBCategoryView, MBGroupQuestionView, \
    MapGroupQuesionDepartmentView, GroupQuestionConfigModel
from .my_views.quiz_views import QuizView
from .my_views.report_views import AnswerLog, DailyReport, MBCheckin, MBReasonView
from .my_views.time_views import MBDimTimeView

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# config question
appbuilder.add_view(
    MBCategoryView,
    "Thể loại",
    icon="fa-sitemap",
    category_icon="fa-gears",
    category="Cấu hình"
)
appbuilder.add_view(
    MBQuestionsView,
    "Câu hỏi",
    icon="fa-database",
    category="Cấu hình"
)
#
# appbuilder.add_view(
#     MBCategoryConfigView,
#     "Cấu hình câu hỏi",
#     icon="fa-gear",
#     category="Cấu hình"
# )
appbuilder.add_view_no_menu(GroupQuestionConfigModel)
appbuilder.add_view(
    MBGroupQuestionView,
    "Cấu hình bộ câu hỏi",
    icon="fa-gear",
    category="Cấu hình",
)
appbuilder.add_separator("Cấu hình")
appbuilder.add_view(
    MapGroupQuesionDepartmentView,
    "Cấu hình bộ câu hỏi theo Phòng/Line",
    icon="fa-gear",
    category="Cấu hình",
)
# config manager
appbuilder.add_separator("Cấu hình")
appbuilder.add_view(
    EmployeesView,
    "Nhân viên",
    icon="fa-user",
    category="Cấu hình"
)

appbuilder.add_view(
    ManagersView,
    "Cán bộ quản lý",
    icon="fa-user-secret",
    category="Cấu hình"
)

appbuilder.add_view(
    DepartmentsView,
    "Phòng - Line",
    icon="fa-institution",
    category="Cấu hình"
)

# config time
appbuilder.add_separator("Cấu hình")
# appbuilder.add_view(
#     MBDimTimeView,
#     "Thời gian gửi báo cáo",
#     icon="fa-calendar",
#     category="Cấu hình"
# )

appbuilder.add_view(
    MBReasonView,
    "Cấu hình lí do",
    icon="fa-calendar",
    category="Cấu hình"
)
# config report
appbuilder.add_view_no_menu(
    MBCheckin,
    "mbcheckin",
)

appbuilder.add_view(DailyReport, "Theo ngày", icon="fa-calendar", category_icon="fa-calendar", category="Báo cáo")
appbuilder.add_separator("Báo cáo")
appbuilder.add_view(AnswerLog, "Log Answers", icon="fa-pencil", category="Báo cáo")

# game
appbuilder.add_view(QuizView, "Bắt đầu", icon="fa-hourglass-start", category_icon="fa-check-square-o",
                    category="Check In")

# API
quiz_api = QuizApi()
appbuilder.add_api(quiz_api)

appbuilder.add_separator("Cấu hình")
appbuilder.add_view(
    MBImagesView, "Quản lý ảnh", icon="fa-file-image-o", category="Cấu hình"
)

appbuilder.add_separator("Cấu hình")
appbuilder.add_view(
    PageTypeView, "Phân loại trang", icon="fa-cogs", category="Cấu hình"
)

appbuilder.add_view(
    PageConfigView, "Quản lý trang", icon="fa-file", category="Cấu hình"
)

# OS
# appbuilder.add_separator("Out Source")
# OS
# appbuilder.add_separator("Out Source")
appbuilder.add_view(
    MBOSReasonView, "OS - Cấu hình lý do", icon="fa-calendar", category="OS"
)
appbuilder.add_view(
    MBHolidayView, "OS - Cấu hình ngày", icon="fa-calendar", category="OS"
)
appbuilder.add_view(
    MapOSReasonWorkTimeView, "OS - Công thức tính công", icon="fa-calendar", category="OS"
)
appbuilder.add_view(
    MBEmployeesOSView, "OS - Nhân sự OS", icon="fa-user", category="OS", category_icon="fa-user-o"
)
appbuilder.add_view(
    MBOSDepartmentsView, "OS - Phòng ban quản lý", icon="fa-institution", category="OS"
)
appbuilder.add_view(
    MBOSManagersView, "OS -Cán bộ quản lý", icon="fa-institution", category="OS"
)
appbuilder.add_view_no_menu(
    MBOSCheckin,
    "mboscheckin",
)
appbuilder.add_view(
    MBOSDailyReport, "OS - Báo cáo theo ngày", icon="fa-calendar", category="OS"
)

# db.create_all()
