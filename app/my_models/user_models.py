from app.my_models.default_models import DefaultModel


class UserModel(DefaultModel):
    def get_user(self, username):
        data = {
            "username" : username
        }
        query = '''
                SELECT username, ho_ten, department_id, ngaysinh
                FROM `mb_employee` e
                where username = :username
                LIMIT 1
                '''
        # create a Session
        session = self.get_session()
        res = None
        try:
            res = session.execute(query,data)
            for r in res:
                # print(r)
                return {
                    "username": r["username"],
                    "ho_ten": r["ho_ten"],
                    "department_id": r["department_id"],
                    "ngaysinh": r["ngaysinh"],
                }
        finally:
            if res is not None:
                res.close()
