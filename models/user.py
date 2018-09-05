from database import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avatarUrl = db.Column(db.String(200), nullable=False)
    nickName = db.Column(db.String(30), nullable=False)
    openId = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    gender = db.Column(db.Integer)
    province = db.Column(db.String(30))
    sharedNum = db.Column(db.Integer, default=0)

    def __init__(self, avatarUrl, city, country, gender, nickName, province, openId):
        self.avatarUrl = avatarUrl
        self.city = city
        self.country = country
        self.gender = gender
        self.nickName = nickName
        self.province = province
        self.openId = openId
        self.sharedNum = 0

    def __repr__(self):
        return '<User {} {}>'.format(self.nickName, self.openId)
