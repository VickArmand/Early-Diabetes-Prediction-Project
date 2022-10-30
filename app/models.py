from datetime import datetime
from flask import session
from flask_login import UserMixin
# TimedJSONWebSignatureSerializer
from app import db,login_manager
from flask import current_app
from itsdangerous import TimedSerializer as Serializer
@login_manager.user_loader
def load_user(patient_id): 
    if "account_type" in session:
        if session["account_type"] == "Admin":
            return Admins.query.get(int(patient_id))
        elif session["account_type"] == "Patient":
            return Patients.query.get(int(patient_id))
        elif session["account_type"] == "Doctor":
            return Doctors.query.get(int(patient_id))
        else:
            return None
    else:
        return None
class Patients(db.Model, UserMixin):
    id=db.Column("id",db.Integer,primary_key=True)
    fname=db.Column("firstname",db.String(100),nullable=False)
    lname=db.Column("lastname",db.String(100),nullable=False)
    email=db.Column("email",db.String(100), unique=True, nullable=False)
    gender=db.Column("gender",db.String(20),nullable=False)
    dateofbirth=db.Column("DoB",db.DateTime,nullable=False)
    contact=db.Column("contact",db.String(20),nullable=False)
    county=db.Column("county",db.String(20),nullable=False)
    area=db.Column("Region",db.String(20),nullable=False)
    predpatientid=db.relationship('Predictions', backref='predictedpat',lazy=True)
    registeredpatientid=db.relationship('PatientCredentials', backref='registeredpat',lazy=True)
    patientmsgid=db.relationship('PatientMessages', backref='recipientpat',lazy=True)
    def get_reset_token(self,expires_sec=1800):
        s=Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    @staticmethod
    def verify_reset_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Patients.query.get(user_id)

class Admins(db.Model,UserMixin):
    id=db.Column("id",db.Integer,primary_key=True)
    fname=db.Column("firstname",db.String(100),nullable=False)
    lname=db.Column("lastname",db.String(100),nullable=False)
    email=db.Column("email",db.String(100), unique=True, nullable=False)
    gender=db.Column("gender",db.String(20),nullable=False)
    dateofbirth=db.Column("DoB",db.DateTime,nullable=False)
    contact=db.Column("contact",db.String(20),nullable=False)
    county=db.Column("county",db.String(20),nullable=False)
    area=db.Column("Region",db.String(20),nullable=False)
    registeredadminid=db.relationship('AdminCredentials', backref='registeredadmin',lazy=True)

class Doctors(db.Model,UserMixin):
    id=db.Column("id",db.Integer,primary_key=True)
    fname=db.Column("firstname",db.String(100),nullable=False)
    lname=db.Column("lastname",db.String(100),nullable=False)
    email=db.Column("email",db.String(100), unique=True, nullable=False)
    gender=db.Column("gender",db.String(20),nullable=False)
    dateofbirth=db.Column("DoB",db.DateTime,nullable=False)
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
    
class AdminCredentials(db.Model):
    adminid=db.Column("id",db.Integer,primary_key=True)
    uname=db.Column("username",db.String(20),unique=True, nullable=False)
    password=db.Column("password",db.String(20),nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status=db.Column(db.String(20),nullable=False,default="Activated")
    adminregistered=db.Column(db.Integer,db.ForeignKey('admins.id'),nullable=False)
    role=db.Column("role",db.String(20),nullable=False,default="General Admin")

class DoctorCredentials(db.Model):
    doctorid=db.Column("id",db.Integer,primary_key=True)
    uname=db.Column("username",db.String(20),unique=True, nullable=False)
    password=db.Column("password",db.String(20),nullable=False)
    specialty=db.Column("specialty",db.String(20),nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status=db.Column(db.String(20),nullable=False,default="Activated")
    doctorregistered=db.Column(db.Integer,db.ForeignKey('doctors.id'),nullable=False)

class Predictions(db.Model):
    id=db.Column("id",db.Integer,primary_key=True)
    pregnancies=db.Column("pregnancies",db.Float,nullable=False)
    glucose=db.Column("glucose",db.Float,nullable=False)
    insulin=db.Column("insulin",db.Float,nullable=False)
    height=db.Column("height",db.Float,nullable=False)
    weight=db.Column("weight",db.Float,nullable=False)
    bmi=db.Column("BMI",db.Float,nullable=False)
    age=db.Column("age",db.Integer,nullable=False)
    pedigree=db.Column("pedigree",db.Integer,nullable=False)
    # bloodpressure=db.Column("BloodPressure",db.Float,nullable=False)
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
