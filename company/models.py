from exts import db



class UserModel(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)

class NewsModel(db.Model):
    __tablename__='news'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    # image_name=db.Column(db.String(200))
    image=db.Column(db.LargeBinary(length=204800))
    content=db.Column(db.String(1000),nullable=False)

class AdvertisementModel(db.Model):
    __tablename__='advertisement'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    picture_name=db.Column(db.String(100),nullable=False)
    picture=db.Column(db.LargeBinary(length=204800),nullable=False)
