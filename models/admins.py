from app import db
class Admins(db.Model,db):
    _id= db.Column("id",db.Integer,primary_key=True)
    fname=db.Column("firstname",db.String(100))
    lname=db.Column("lastname",db.String(100))
    email=db.Column("email",db.String(100))
    password=db.Column("password",db.String(20))
    gender=db.Column("gender",db.String(20))
    dateofbirth=db.Column("DoB",db.String(20))
    contact=db.Column("contact",db.String(20))
    county=db.Column("county",db.String(20))
    area=db.Column("Region",db.String(20))
    uname=db.Column("username",db.String(20))
    password=db.Column("password",db.String(20))
