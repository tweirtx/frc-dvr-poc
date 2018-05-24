import db


class streamdb(db.DatabaseObject):
    __tablename__ = 'streamstarts'
    eventkey = db.Column(db.String)
    starttime = db.Column(db.Integer)
    day = db.Column(db.String)
    primary_key = db.Column(db.Integer, primary_key=True, autoincrement=True)


db.DatabaseObject.metadata.create_all()
