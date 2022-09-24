from datetime import datetime
from app import db
class Patients(db.Model):
    id=db.Column("id",db.Integer,primary_key=True)
    fname=db.Column("firstname",db.String(100),nullable=False)
    lname=db.Column("lastname",db.String(100),nullable=False)
    email=db.Column("email",db.String(100), unique=True, nullable=False)
    gender=db.Column("gender",db.String(20),nullable=False)
    dateofbirth=db.Column("DoB",db.String(20),nullable=False)
    contact=db.Column("contact",db.String(20),nullable=False)
    county=db.Column("county",db.String(20),nullable=False)
    area=db.Column("Region",db.String(20),nullable=False)
    predpatientid=db.relationship('Predictions', backref='predictedpat',lazy=True)
    registeredpatientid=db.relationship('PatientCredentials', backref='registeredpat',lazy=True)
    patientmsgid=db.relationship('PatientMessages', backref='recipient',lazy=True)
    def __init__(self,id,fname,lname,email,gender,dateofbirth,contact,county,area):
        self.id=id
        self.fname=fname
        self.lname=lname
        self.email=email
        self.gender=gender
        self.dateofbirth=dateofbirth
        self.contact=contact
        self.county=county
        self.area=area
class Admins(db.Model):
    id=db.Column("id",db.Integer,primary_key=True)
    fname=db.Column("firstname",db.String(100),nullable=False)
    lname=db.Column("lastname",db.String(100),nullable=False)
    email=db.Column("email",db.String(100), unique=True, nullable=False)
    gender=db.Column("gender",db.String(20),nullable=False)
    dateofbirth=db.Column("DoB",db.String(20),nullable=False)
    contact=db.Column("contact",db.String(20),nullable=False)
    def __init__(self,id,fname,lname,email,gender,dateofbirth,contact):
        self.id=id
        self.fname=fname
        self.lname=lname
        self.email=email
        self.gender=gender
        self.dateofbirth=dateofbirth
        self.contact=contact
class Doctors(db.Model):
    id=db.Column("id",db.Integer,primary_key=True)
    fname=db.Column("firstname",db.String(100),nullable=False)
    lname=db.Column("lastname",db.String(100),nullable=False)
    email=db.Column("email",db.String(100), unique=True, nullable=False)
    gender=db.Column("gender",db.String(20),nullable=False)
    dateofbirth=db.Column("DoB",db.String(20),nullable=False)
    contact=db.Column("contact",db.String(20),nullable=False)
    county=db.Column("county",db.String(20),nullable=False)
    area=db.Column("Region",db.String(20),nullable=False)
    registereddoctorid=db.relationship('DoctorCredentials', backref='registereddoc',lazy=True)
 
class PatientCredentials(db.Model):
    patientid=db.Column("id",db.Integer,primary_key=True)
    uname=db.Column("username",db.String(20), unique=True, nullable=False)
    password=db.Column("password",db.String(20),nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status=db.Column(db.String(20),nullable=False,default="Activated")
    patientregistered=db.Column(db.Integer,db.ForeignKey('patients.id'),nullable=False)

    def __init__(self,patientid,uname,password):
        self.id=patientid
        self.uname=uname
        self.password=password
class AdminCredentials(db.Model):
    adminid=db.Column("id",db.Integer,primary_key=True)
    uname=db.Column("username",db.String(20),unique=True, nullable=False)
    password=db.Column("password",db.String(20),nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status=db.Column(db.String(20),nullable=False,default="Activated")
    adminregistered=db.Column(db.Integer,db.ForeignKey('admins.id'),nullable=False)
    role=db.Column("role",db.String(20),nullable=False,default="General Admin")
    def __init__(self,adminid,uname,password):
        self.id=adminid
        self.uname=uname
        self.password=password
class DoctorCredentials(db.Model):
    doctorid=db.Column("id",db.Integer,primary_key=True)
    uname=db.Column("username",db.String(20),unique=True, nullable=False)
    password=db.Column("password",db.String(20),nullable=False)
    speciality=db.Column("specialty",db.String(20),nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status=db.Column(db.String(20),nullable=False,default="Activated")
    doctorregistered=db.Column(db.Integer,db.ForeignKey('doctors.id'),nullable=False)

    def __init__(self,doctorid,uname,password):
        self.id=doctorid
        self.uname=uname
        self.password=password
class Predictions(db.Model):
    id=db.Column("id",db.Integer,primary_key=True)
    glucose=db.Column("glucose",db.Float,nullable=False)
    insulin=db.Column("insulin",db.Float,nullable=False)
    bmi=db.Column("BMI",db.Float,nullable=False)
    age=db.Column("age",db.Integer,nullable=False)
    bloodpressure=db.Column("BloodPressure",db.Float,nullable=False)
    outcome=db.Column("outcome",db.Integer,nullable=False)
    date_predicted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    patientpred=db.Column(db.Integer,db.ForeignKey('patients.id'),nullable=False)
class PatientMessages(db.Model):
    id=db.Column("id",db.Integer,primary_key=True)
    title=db.Column("title",db.String(50), nullable=False)
    body=db.Column("body",db.String(1000),nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status=db.Column(db.String(20),nullable=False,default="Sent")
    recipient=db.Column(db.Integer,db.ForeignKey('patients.id'),nullable=False)
