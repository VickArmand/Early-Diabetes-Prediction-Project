from flask import Flask
import numpy as np
import xgboost as xgb
import os
import pickle as pk
# predict,datapreprocessing,train,modelgeneration,computemetrics
from app.sendnotification import sendmail
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///diabetespred.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY']='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
db=SQLAlchemy(app)
from datetime import timedelta
app.permanent_session_lifetime=timedelta(hours=3)
from app import routes
