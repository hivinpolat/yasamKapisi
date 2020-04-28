from yasamkapisi.db import db

#Modeller oluşturuldu.
class User(db.Document):
    name = db.StringField(required=True)
    surname = db.StringField(required=True)
    phone = db.StringField(required=True,max_length=10)
    mail = db.EmailField(required=True,unique=True)
    workspace = db.StringField(required=True)
    gender = db.StringField(required=True)
    birthday = db.DateTimeField()
    tc = db.StringField(required=True,max_length=11)
    username = db.StringField(required=True,unique=True)
    password = db.StringField(required=True)