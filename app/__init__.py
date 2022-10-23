from flask import Flask,session
import numpy as np
import os
import pickle as pk
# predict,datapreprocessing,train,modelgeneration,computemetrics
from app.sendnotification import sendmail
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
session= session
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///diabetespred.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY']='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
bcrypt=Bcrypt(app)
db=SQLAlchemy(app)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='warning'
from datetime import timedelta
app.permanent_session_lifetime=timedelta(hours=3)
from app import routes
