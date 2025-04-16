from app import db


class DefaultModel:
    def __init__(self):
        self.db = db
        # create a configured "Session" class
        # self.Session = sessionmaker(bind=self.db.engine)

    def get_session(self):
        # return self.Session();
        return self.db.session