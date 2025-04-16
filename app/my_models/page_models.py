from flask import url_for
from flask_appbuilder import Model
from flask_appbuilder.filemanager import get_file_original_name
from flask_appbuilder.models.mixins import AuditMixin, FileColumn
from markupsafe import Markup
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.my_models.default_models import DefaultModel


class MBImages(AuditMixin, Model):
    __tablename__ = "mb_images"
    id = Column(Integer, primary_key=True)
    file = Column(FileColumn, nullable=False)
    description = Column(String(150))

    def download(self):
        return Markup(
            '<a href="'
            + url_for("MBImagesView.download", filename=str(self.file))
            + '">Download</a>'
        )

    def file_name(self):
        return get_file_original_name(str(self.file))

    def __repr__(self):
        return get_file_original_name(str(self.file))


class PageType(Model):
    __tablename__ = "page_type"
    id = Column(String(200), primary_key=True)
    description = Column(String(150))

    def __repr__(self):
        if self.description is not None:
            return self.description
        else:
            return self.id


class MBPageConfig(AuditMixin, Model):
    __tablename__ = "mb_page_config"
    id = Column(Integer, primary_key=True)
    page_type_id = Column(String(200), ForeignKey(PageType.id))
    page_type = relationship(PageType)
    image_id = Column(Integer, ForeignKey(MBImages.id))
    image = relationship(MBImages)
    description = Column(String(2000))

    def __repr__(self):
        if self.description is not None:
            return self.description
        else:
            return str(self.id)


class ApiImageModel(DefaultModel):
    def get_image(self, page_type):
        data = {
            "page_type_id": page_type
        }
        query = '''
            SELECT t1.image_id, t2.file
            FROM mb_page_config t1 
            JOIN`mb_images` t2
            ON t1.image_id = t2.id
            WHERE page_type_id = :page_type_id
            ORDER BY t1.`changed_on` DESC
            LIMIT 1
        '''
        session = self.get_session()
        try:
            res = session.execute(query, data)
            for r in res:
                return str(r["file"])
        except Exception:
            raise
        finally:
            if res is not None:
                res.close()