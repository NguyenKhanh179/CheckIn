from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.my_models.question_models import MBCategoryConfig, MBQuestions, MBCategory, MBGroupQuestions, \
    MapGroupQuestionDepartment, GroupQuestionConfig


#
#
# class MBCategoryConfigView(ModelView):
#     datamodel = SQLAInterface(MBCategoryConfig)
#
#     label_columns = {}
#     list_columns = ['category', 'questions', 'status', 'created_date', 'updated_date']
#     # add_columns = ['category', 'questions', 'is_active']
#     # related_views = [ManagersView, EmployeesView]
#
#     show_fieldsets = [
#         (
#             'Info',
#             {'fields': ['category', 'questions', 'status', 'created_date', 'updated_date']}
#         )
#     ]

class MBQuestionsView(ModelView):
    datamodel = SQLAInterface(MBQuestions)
    show_title = "Danh sách câu hỏi"
    list_title = "Danh sách câu hỏi"
    label_columns = {}
    list_columns = ['id', 'category', 'type', "difficulty", "content"]
    # related_views = [ManagersView, EmployeesView]
    edit_columns = ['id', 'category', 'type', "difficulty", "content",
                    'answer1', 'answer2', 'answer3', 'answer4', 'correct_answer'

                    ]

    show_fieldsets = [
        (
            'Question',
            {'fields': ['id', 'category', 'type', "difficulty", "content"]}
        ),
        (
            'Answer',
            {'fields': ['answer1', 'answer2', 'answer3', 'answer4']}
        ),
        (
            'Correct Answer',
            {'fields': ['correct_answer']}
        ),
    ]


class MBCategoryView(ModelView):
    datamodel = SQLAInterface(MBCategory)

    label_columns = {}
    list_columns = ['category_id', 'name']
    add_columns = ['category_id', 'name']
    related_views = [MBQuestionsView]

    show_fieldsets = [
        (
            'Info',
            {'fields': ['category_id', 'name', 'created_date', 'updated_date']}
        )
    ]
#
#
class GroupQuestionConfigModel(ModelView):
    datamodel = SQLAInterface(GroupQuestionConfig)
    label_columns = {'count_questions': 'Số câu hỏi', 'category': 'Chủ đề', 'group_question': 'Nhóm câu hỏi'}
    list_columns = ['id', 'group_question', 'category', 'count_questions', 'status']
    add_columns = ['group_question', 'category', 'count_questions']
    edit_columns =  ['group_question', 'category', 'count_questions', 'status']
    list_title = "Cấu hình bộ câu hỏi"
    add_title = "Thêm mới chủ đề"
    edit_title = "Thay đổi cấu hình chủ đề"


class MBGroupQuestionView(ModelView):
    datamodel = SQLAInterface(MBGroupQuestions)

    list_title = "Danh sách bộ câu hỏi"
    edit_title = "Thay đổi Bộ câu hỏi"
    add_title =  "Thêm bộ câu hỏi"
    label_columns = {'status_desc': 'Trạng thái', 'description' : "Chú thích",
                     "created_date": 'Ngày tạo'}
    list_columns = ['description', "status_desc", "created_date"]
    edit_columns = ['description', "status_desc", "created_date"]
    add_columns = ['description']

    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'
    related_views = [GroupQuestionConfigModel]

class MapGroupQuesionDepartmentView(ModelView):
    show_title = "Cấu hình bộ câu hỏi theo đơn vị"
    list_title = "Danh sách bộ câu hỏi theo đơn vị"
    datamodel = SQLAInterface(MapGroupQuestionDepartment)
    label_columns = {'status': 'Trạng thái',
                     "created_date": 'Ngày tạo','group_question': 'Nhóm câu hỏi'}

    list_columns = ["id", "group_question",'department', 'status','created_date', 'updated_date']
    add_columns = [ "group_question", "department"]
    edit_columns = [ "group_question","department", 'status']
