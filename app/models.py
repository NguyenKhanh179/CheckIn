from app.my_models.log_models import APILogModel
from app.my_models.os_models import MBOSDailyReportModels
from app.my_models.page_models import ApiImageModel
from app.my_models.question_models import ApiQuestionModel
from app.my_models.report_models import DailyReportModels
from app.my_models.user_models import UserModel

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
api_log_model = APILogModel()
api_image_model= ApiImageModel()
api_question_model=ApiQuestionModel()
api_daily_report_model = DailyReportModels()
user_model = UserModel()
api_os_daily_report_model = MBOSDailyReportModels()
