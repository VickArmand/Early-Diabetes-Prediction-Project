from flask import render_template,request,url_for,redirect,session,flash,abort,jsonify
from app import mail
from app.models import *
from flask_mail import Message
def send_reset_mail(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request',sender='',recipients=[user.email])
    msg.body=f'''
    To reset your password visit the following link:
    {url_for('patients.reset_token',token=token,_external=True)}

    If you did not make this request then ignore this message
    '''
    mail.send(msg)