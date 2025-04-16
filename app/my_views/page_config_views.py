from flask_appbuilder import CompactCRUDMixin, ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app.my_models.page_models import MBImages, PageType, MBPageConfig


class MBImagesView(CompactCRUDMixin, ModelView):
    datamodel = SQLAInterface(MBImages)

    label_columns = {"file_name": "File Name", "download": "Download"}
    add_columns = ["file", "description"]
    edit_columns = ["file", "description"]
    list_columns = ["file_name", "download", "created_by", "created_on", "changed_by", "changed_on"]
    show_fieldsets = [
        ("Info", {"fields": ["file", "description", "download"]}),
        (
            "Audit",
            {
                "fields": ["created_by", "created_on", "changed_by", "changed_on"],
                "expanded": False,
            },
        ),
    ]


class PageTypeView(ModelView):
    datamodel = SQLAInterface(PageType)

    label_columns = {}
    add_columns = ["id", "description"]
    edit_columns = ["description"]
    show_columns = ["id", "description"]
    list_columns = ["id", "description"]


class PageConfigView(ModelView):
    datamodel = SQLAInterface(MBPageConfig)
    label_columns = {"page_type": "Trang", "description": "Chú thích", "image": "Ảnh"}
    add_columns = ["page_type", "image", "description"]
    edit_columns = ["id", "page_type", "image", "description"]
    list_columns = ["id", "page_type", "image", "description"]
    show_fieldsets = [
        ("Info", {"fields": ["id", "page_type", "image", "description"]}),
        (
            "Audit",
            {
                "fields": ["created_by", "created_on", "changed_by", "changed_on"],
                "expanded": False,
            },
        ),
    ]