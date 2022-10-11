from app.models import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, RadioField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError, Regexp
import phonenumbers
from datetime import datetime
class RegistrationForm(FlaskForm):
    firstname=StringField('First Name',validators=[DataRequired(),Length(min=5, max=20)])
    lastname=StringField('Last Name',validators=[DataRequired(),Length(min=5, max=20)])
    username=StringField('Username',validators=[DataRequired(),Length(min=5, max=20)])
    gender=RadioField('Gender',validators=[DataRequired()], choices=[('Male','Male'),('Female','Female')])
    county=SelectField('County',validators=[DataRequired()], choices=[('Mombasa','Mombasa'),('Kwale','Kwale'),('Kilifi','Kilifi'),('Tana-River','Tana-River'),('Lamu','Lamu'),('Taita Taveta','Taita Taveta'),('Garissa','Garissa'),('Wajir','Wajir'),('Mandera','Mandera'),('Marsabit','Marsabit'),('Isiolo','Isiolo'),('Meru','Meru'),('Tharaka-Nithi','Tharaka-Nithi'),('Embu','Embu'),('Kitui','Kitui'),('Machakos','Machakos'),('Makueni','Makueni'),('Nyandarua','Nyandarua'),('Nyeri','Nyeri'),('Kirinyaga','Kirinyaga'),("Murang'a","Murang'a"),('Kiambu','Kiambu'),('Turkana','Turkana'),('West Pokot','West Pokot'),('Samburu','Samburu'),('Trans-Nzoia','Trans-Nzoia'),('Uasin Gishu','Uasin Gishu'),('Elgeyo-Marakwet','Elgeyo-Marakwet'),('Nandi','Nandi'),('Baringo','Baringo'),('Laikipia','Laikipia'),('Nakuru','Nakuru'),('Narok','Narok'),('Kajiado','Kajiado'),('Kericho','Kericho'),('Bomet','Bomet'),('Kakamega','Kakamega'),('Vihiga','Vihiga'),('Bungoma','Bungoma'),('Busia','Busia'),('Siaya','Siaya'),('Kisumu','Kisumu'),('Homa Bay','Homa Bay'),('Migori','Migori'),('Kisii','Kisii'),('Nyamira','Nyamira'),('Nairobi','Nairobi'),])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    DoB=DateField('Date of Birth (MM-DD-YYYY)',validators=[DataRequired()])
    area=StringField('Residential Area',validators=[DataRequired()])
    contact=StringField('Contact',validators=[DataRequired(),Regexp('^(\\+\\d{1,3}( )?)?(\\d{3}[ ]?){2}\\d{3}$')] )
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('REGISTER')

    def validate_phone(self,contact):
        ispresentPatient=Patients.query.filter_by(contact=contact.data).first()
        if ispresentPatient :
            raise ValidationError('Phone Number Already exists')
        
    def validate_username(self,username):
        ispresentPatient=PatientCredentials.query.filter_by(uname=username.data).first()
        if ispresentPatient :
            raise ValidationError('Username already taken')
    def validate_email(self,email):
        ispresentPatient=Patients.query.filter_by(email=email.data).first()
        if ispresentPatient :
            raise ValidationError('Email Already exists')
    def validate_date(self,DoB):
        if datetime.strptime(str(DoB.data),'%Y-%m-%d').year >= datetime.now().year:
            raise ValidationError("The date cannot be in the future!")
        agediff=datetime.now().year - datetime.strptime(DoB.data,'%Y-%m-%d').year
        print(f'Year is {agediff}')
        if agediff < 10:
            raise ValidationError("Age too low for registration.")
class DoctorRegistrationForm(RegistrationForm):
    specialty=SelectField('Specialty',validators=[DataRequired()], choices=[('Pharmacy','Pharmacy'),('Surgery','Surgery'),('Laboratory','Laboratory'),('Consultant','Consultant'),('Treatment','Treatment')])
    def validate_phone(self,contact):
        ispresentPatient=Doctors.query.filter_by(contact=contact.data).first()
        if ispresentPatient :
            raise ValidationError('Phone Number Already exists')
        
    def validate_username(self,username):
        ispresentPatient=DoctorCredentials.query.filter_by(uname=username.data).first()
        if ispresentPatient :
            raise ValidationError('Username already taken')
    def validate_email(self,email):
        ispresentPatient=Doctors.query.filter_by(email=email.data).first()
        if ispresentPatient :
            raise ValidationError('Email Already exists')
    def validate_date(self,DoB):
        if datetime.strptime(str(DoB.data),'%Y-%m-%d').year >= datetime.now().year:
            raise ValidationError("The date cannot be in the future!")
        agediff=datetime.now().year - datetime.strptime(DoB.data,'%Y-%m-%d').year
        print(f'Year is {agediff}')
        if agediff < 10:
            raise ValidationError("Age too low for registration.")
            
class AdminRegistrationForm(RegistrationForm):
    role=SelectField('Role',validators=[DataRequired()], choices=[('Super Admin','Super Admin'),('General Admin','General Admin')])
    def validate_phone(self,contact):
        ispresentPatient=Admins.query.filter_by(contact=contact.data).first()
        if ispresentPatient :
            raise ValidationError('Phone Number Already exists')
        
    def validate_username(self,username):
        ispresentPatient=AdminCredentials.query.filter_by(uname=username.data).first()
        if ispresentPatient :
            raise ValidationError('Username already taken')
    def validate_email(self,email):
        ispresentPatient=Admins.query.filter_by(email=email.data).first()
        if ispresentPatient :
            raise ValidationError('Email Already exists')
    def validate_date(self,DoB):
        if datetime.strptime(str(DoB.data),'%Y-%m-%d').year >= datetime.now().year:
            raise ValidationError("The date cannot be in the future!")
        agediff=datetime.now().year - datetime.strptime(DoB.data,'%Y-%m-%d').year
        print(f'Year is {agediff}')
        if agediff < 10:
            raise ValidationError("Age too low for registration.")
class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    remember=BooleanField('Remember Me')
    submit=SubmitField('LOGIN')
    def validate_email(self,email):
        ispresentPatient=Patients.query.filter_by(email=email.data).first()
        if not ispresentPatient :
            raise ValidationError('User does not exist')
class AdminLoginForm(LoginForm):
    def validate_email(self,email):
        ispresentPatient=Admins.query.filter_by(email=email.data).first()
        if not ispresentPatient :
            raise ValidationError('User does not exist')
class DoctorLoginForm(LoginForm):
    def validate_email(self,email):
        ispresentPatient=Doctors.query.filter_by(email=email.data).first()
        if not ispresentPatient :
            raise ValidationError('User does not exist')
class UpdateForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=5, max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    contact=StringField('Contact',validators=[DataRequired(),Regexp('^(\\+\\d{1,3}( )?)?(\\d{3}[ ]?){2}\\d{3}$')] )
    submit=SubmitField('EDIT DETAILS')
class ChangePasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    new_password=PasswordField('New Password',validators=[DataRequired(),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    confirm_new_password=PasswordField('Confirm New Password',validators=[DataRequired(),EqualTo('new_password'),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    submit=SubmitField('CHANGE PASSWORD')
class AdminEditPatients(RegistrationForm):
    status=SelectField('Status',validators=[DataRequired()], choices=[('Activated','Activated'),('Deactivated','Deactivated')])
    submit=SubmitField('UPDATE')
class AdminEditDoctors(DoctorRegistrationForm):
    status=SelectField('Status',validators=[DataRequired()], choices=[('Activated','Activated'),('Deactivated','Deactivated')])
    submit=SubmitField('UPDATE')
class AdminEditAdmins(AdminRegistrationForm):
    status=SelectField('Status',validators=[DataRequired()], choices=[('Activated','Activated'),('Deactivated','Deactivated')])
    submit=SubmitField('UPDATE')