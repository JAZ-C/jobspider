from database import db

class YasiInfo(db.Model):

    __tablename__ = 'infos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cityname = db.Column(db.String(50), nullable=False, unique=True)
    detail = db.Column(db.JSON, nullable=False)

    def __init__(self, cityname, detail):
        self.cityname = cityname
        self.detail = detail

    def __repr__(self):
        return '<Info {}>'.format(self.cityname)
    
    def to_json(self):
        return {
            "cityname": self.cityname,
            "detail": self.detail
        }
