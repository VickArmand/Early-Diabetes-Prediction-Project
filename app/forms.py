from app.models import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, RadioField,IntegerField
from wtforms.widgets import NumberInput
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError, Regexp
import phonenumbers
from datetime import datetime

class RequestResetForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('REQUEST PASSWORD RESET')
    def validate_email(self,email):
        ispresentPatient=Patients.query.filter_by(email=email.data).first()
        if ispresentPatient is None :
            raise ValidationError('There is no account with that email')
class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8, max=20),Regexp("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('RESET PASSWORD')

 