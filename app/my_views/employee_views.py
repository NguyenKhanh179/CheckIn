from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.my_models.employee_models import MBEmployee, MBDepartments, MBManagers


class EmployeesView(ModelView):
    datamodel = SQLAInterface(MBEmployee)

    label_columns = {'ho_ten': 'Họ tên',
                     'ten_jira': 'Jira',
                     'chucdanh': 'Chức danh', 'ngayvaomb': 'Ngày vào MB',
                     'ngaysinh': 'Ngày sinh', "status_desc" : "Trạng thái"}
    list_columns = ['username', 'ho_ten', 'department', 'chucdanh','status_desc', 'note']

    add_columns = ['username', 'ho_ten', 'ma_nv', 'ten_jira',
                   'department', 'email', 'chucdanh',
                   'ngayvaomb', 'ngaysinh', 'status_desc', 'note']

    edit_columns =  ['username', 'ho_ten', 'ma_nv', 'ten_jira',
                   'department', 'email', 'chucdanh',
                   'ngayvaomb', 'ngaysinh', 'status_desc', 'note']
    search_columns = [
        'username', 'ho_ten', 'ma_nv', 'ten_jira',
        'department', 'email', 'chucdanh',
        'ngayvaomb', 'ngaysinh', 'status_desc', 'note'
    ]

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['username', 'ho_ten', 'department', 'status_desc']}
        ),
        (
            'Personal Info',
            {'fields': ['ma_nv', 'ten_jira', 'ho_ten',
                        'department', 'email', 'chucdanh',
                        'ngayvaomb', 'ngaysinh', 'note'], 'expanded': False}
        ),
    ]


class DepartmentsView(ModelView):
    datamodel = SQLAInterface(MBDepartments)
    label_columns = {'name': 'Tên','donvi': 'Đơn vị',
                     'donvi_tt1': 'Đơn vị trực thuộc cấp 1',
                     'donvi_tt2': 'Đơn vị trực thuộc cấp 2',
                     'donvi_tt3': 'Đơn vị trực thuộc cấp 3',
                     }
    list_columns = ['name','donvi', 'donvi_tt1', 'donvi_tt2', 'donvi_tt3', 'status','level']
    related_views = [EmployeesView]


class ManagersView(ModelView):
    datamodel = SQLAInterface(MBManagers)
    # base_filters = [
    #     ['username', FilterStartsWith,'a']
    # ]
    label_columns = {}
    list_columns = ['id', 'username','created_date', 'updated_date',
                    'manager', 'department']
    add_columns = ['manager', 'department']
    edit_columns = ['manager', 'department']

    # related_views = [DepartmentsView]

    show_fieldsets = [
        (
            'Info',
            {'fields': ['id', 'username', 'department',
                        'created_date', 'updated_date', 'manager', 'department']}
        )
    ]