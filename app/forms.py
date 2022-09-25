from app.models import *
from wsgiref.validate import validator
from xml.dom import ValidationErr
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, RadioField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError, Regexp
import phonenumbers

class RegistrationForm(FlaskForm):
    firstname=StringField('First Name',validators=[DataRequired(),Length(min=5, max=20)])
    lastname=StringField('Last Name',validators=[DataRequired(),Length(min=5, max=20)])
    username=StringField('Username',validators=[DataRequired(),Length(min=5, max=20)])
    gender=RadioField('Gender',validators=[DataRequired()], choices=[('Male','Male'),('Male','Female')])
    county=SelectField('County',validators=[DataRequired()], choices=[('Male','Male'),('Male','Female')])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    DoB=DateField('Date of Birth',validators=[DataRequired()])
    area=StringField('Residential Area',validators=[DataRequired()])
    contact=StringField('Contact',validators=[DataRequired(),Regexp('^(\\+\\d{1,3}( )?)?(\\d{3}[ ]?){2}\\d{3}$')] )
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('REGISTER')
    def validate_username(self,username):
        ispresentPatient=PatientCredentials.query.filter_by(username=username.data).first()
        if ispresentPatient :
            raise ValidationError('Username already taken')
    def validate_email(self,email):
        ispresentPatient=Patients.query.filter_by(email=email.data).first()
        if ispresentPatient :
            raise ValidationError('Email Already exists')

   
class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('LOGIN')

class UpdateForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=5, max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    contact=StringField('Contact',validators=[DataRequired(),Regexp('^(\\+\\d{1,3}( )?)?(\\d{3}[ ]?){2}\\d{3}$')] )
    submit=SubmitField('EDIT DETAILS')
class ChangePassword(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    new_password=PasswordField('New Password',validators=[DataRequired()])
    confirm_new_password=PasswordField('Confirm New Password',validators=[DataRequired(),EqualTo('new_password')])
    submit=SubmitField('CHANGE PASSWORD')