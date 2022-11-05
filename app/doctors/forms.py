from app.models import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, RadioField,IntegerField,validators
from wtforms.widgets import NumberInput
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError, Regexp
import phonenumbers
from datetime import datetime
class DoctorLoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    remember=BooleanField('Remember Me')
    submit=SubmitField('LOGIN')
    def validate_email(self,email):
        ispresentPatient=Doctors.query.filter_by(email=email.data).first()
        if not ispresentPatient :
            raise ValidationError('User does not exist')

class DoctorPasswordForm(FlaskForm):    
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    new_password=PasswordField('New Password',validators=[DataRequired(),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    confirm_new_password=PasswordField('Confirm New Password',validators=[DataRequired(),EqualTo('new_password'),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    submit=SubmitField('CHANGE PASSWORD')

class HealthPredictionForm(FlaskForm):
    patientsselect=SelectField('Select A Patient',validators=[DataRequired()], choices=[('','---Select A Patient---')])
    # pregnancies=SelectField('Number of times pregnant',validators=[DataRequired()], choices=[('','-- SELECT A VALUE --'),('None','None'),('Greater than or equal to one and less than five','Greater than or equal to one and less than five'),('Greater than or equal to five','Greater than or equal to five')])
    pregnancies=IntegerField('Number of times pregnant',widget=NumberInput(step=1, min=0, max=20), validators=[DataRequired()])
    height=SelectField('Height of the Patient',validators=[DataRequired()], choices=[('','-- SELECT A VALUE --'),('Less than or equal to 100cm','Less than or equal to 100cm'),('Greater than 100cm and less than 200cm','Greater than 100cm and less than 200cm'),('Greater than or equal to 200cm','Greater than or equal to 200cm')])
    weight=SelectField('Weight of the Patient',validators=[DataRequired()], choices=[('','-- SELECT A VALUE --'),('Less than 50kg','Less than 50kg'),('Greater than or equal to 50kg and less than 84kg','Greater than or equal to 50kg and less than 84kg'),('Greater than or equal to 84kg and less than 112kg','Greater than or equal to 84kg and less than 112kg'),('Greater than 112kg','Greater than 112kg')])
    glucose=SelectField('Glucose level of the Patient',validators=[DataRequired()], choices=[('','-- SELECT A VALUE --'),('Less than or equal to 80 mg/dl','Less than or equal to 80 mg/dl'),('Greater than 80 mg/dl and less than or equal to 100 mg/dl','Greater than 80 mg/dl and less than or equal to 100 mg/dl'),('Greater than 100 mg/dl and less than or equal to 120 mg/dl','Greater than 100 mg/dl and less than or equal to 120 mg/dl'),('Greater than 120 mg/dl and less than or equal to 130 mg/dl','Greater than 120 mg/dl and less than or equal to 130 mg/dl'),('Greater than 130 mg/dl and less than or equal to 145 mg/dl','Greater than 130 mg/dl and less than or equal to 145 mg/dl'),('Greater than 145 mg/dl and less than or equal to 160 mg/dl','Greater than 145 mg/dl and less than or equal to 160 mg/dl'),('Greater than 160 mg/dl and less than or equal to 170 mg/dl','Greater than 160 mg/dl and less than or equal to 170 mg/dl'),('Greater than 170 mg/dl','Greater than 170 mg/dl')])
    # bloodpressure=SelectField('Diastolic Blood pressure level of the Patient',validators=[DataRequired()], choices=[('','-- SELECT A VALUE --'),('Less than or equal to 80','Less than or equal to 80'),('Greater than 80','Greater than 80')])
    insulin=SelectField('Insulin level of the Patient',validators=[DataRequired()], choices=[('','-- SELECT A VALUE --'),('Less than or equal to 20 mU/ml','Less than or equal to 20 mU/ml'),('Greater than 20 mU/ml and Less than or equal to 80 mU/ml','Greater than 20 mU/ml and Less than or equal to 80 mU/ml'),
    ('Greater than 80 mU/ml and less than or equal to 150 mU/ml','Greater than 80 mU/ml and less than or equal to 150 mU/ml'),
    ('Greater than 150 mU/ml and less than or equal to 300 mU/ml','Greater than 150 mU/ml and less than or equal to 300 mU/ml'),
    ('Greater than 300 mU/ml and less than or equal to 500 mU/ml','Greater than 300 mU/ml and less than or equal to 500 mU/ml'),
    ('Greater than 500 mU/ml','Greater than 500 mU/ml')])
    pedigree=RadioField('Do you have a close relative with diabetes(Parents or Siblings)',validators=[DataRequired()], choices=[('Yes','Yes'),('No','No')])
    submit=SubmitField('PREDICT')
    def validate_pregnancies(self,patientsselect,pregnancies):
        print("DFGHJKLKJHGFDSDFGH")
        ispresentDoc=Doctors.query.filter_by(id=int(patientsselect.data)).first()
        print(ispresentDoc.gender)
        if ispresentDoc.gender == 'Male' and int(pregnancies.data) != 0:
            raise ValidationError('Invalid pregnancy value for male patient')
class DoctorUpdateForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=3, max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    contact=StringField('Contact',validators=[DataRequired(),Regexp('^(\\+\\d{1,3}( )?)?(\\d{3}[ ]?){2}\\d{3}$')] )
    submit=SubmitField('EDIT DETAILS')
    def validate_phone(self,contact):
        ispresentPatient=Doctors.query.filter_by(contact=contact.data).first()
        if ispresentPatient :
            raise ValidationError('Phone Number Already exists')
    def validate_username(self,username):
        ispresentPatient=DoctorCredentials.query.filter_by(uname=username.data).first()
        if ispresentPatient :
            raise ValidationError('Username exists')
    def validate_email(self,email):
        ispresentPatient=Doctors.query.filter_by(email=email.data).first()
        if ispresentPatient :
            raise ValidationError('Email Already exists')
class ChangePasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    new_password=PasswordField('New Password',validators=[DataRequired(),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    confirm_new_password=PasswordField('Confirm New Password',validators=[DataRequired(),EqualTo('new_password'),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    submit=SubmitField('CHANGE PASSWORD') 
class ReportForm(FlaskForm):
    genderselect=SelectField('Gender',validators=[], choices=[('','---Select A Gender---'),('Male','Male'),('Female','Female')])
    outcomeselect=SelectField('Outcome',validators=[], choices=[('','---Select A Outcome---'),('1','Diabetic'),('0','Non-Diabetic')])
    countyselect=SelectField('County',validators=[], choices=[('','---Select A County---'),('Mombasa','Mombasa'),('Kwale','Kwale'),('Kilifi','Kilifi'),('Tana-River','Tana-River'),('Lamu','Lamu'),('Taita Taveta','Taita Taveta'),('Garissa','Garissa'),('Wajir','Wajir'),('Mandera','Mandera'),('Marsabit','Marsabit'),('Isiolo','Isiolo'),('Meru','Meru'),('Tharaka-Nithi','Tharaka-Nithi'),('Embu','Embu'),('Kitui','Kitui'),('Machakos','Machakos'),('Makueni','Makueni'),('Nyandarua','Nyandarua'),('Nyeri','Nyeri'),('Kirinyaga','Kirinyaga'),("Murang'a","Murang'a"),('Kiambu','Kiambu'),('Turkana','Turkana'),('West Pokot','West Pokot'),('Samburu','Samburu'),('Trans-Nzoia','Trans-Nzoia'),('Uasin Gishu','Uasin Gishu'),('Elgeyo-Marakwet','Elgeyo-Marakwet'),('Nandi','Nandi'),('Baringo','Baringo'),('Laikipia','Laikipia'),('Nakuru','Nakuru'),('Narok','Narok'),('Kajiado','Kajiado'),('Kericho','Kericho'),('Bomet','Bomet'),('Kakamega','Kakamega'),('Vihiga','Vihiga'),('Bungoma','Bungoma'),('Busia','Busia'),('Siaya','Siaya'),('Kisumu','Kisumu'),('Homa Bay','Homa Bay'),('Migori','Migori'),('Kisii','Kisii'),('Nyamira','Nyamira'),('Nairobi','Nairobi'),])
    submit=SubmitField('FILTER')
