from flask import render_template,request,url_for,redirect,session,flash,abort,jsonify
import os
import json
import sqlite3
import io
from app import app,pk,np,db,bcrypt,mail
from app import sendnotification
from app.models import *
from flask_login import login_user,current_user,logout_user,login_required
import random
from app.sendnotification import *
from flask_mail import Message
# Constructing web routes
datasetpath='./app/static/Datasets'
datasetfile= "diabetes.csv"
datasetpathfile=os.path.join(datasetpath,datasetfile)
modelspath='./app/static/ML Model'
modelfile= "diabetespredmodelusingxgboost.pkl"
modelpathfile=os.path.join(modelspath,modelfile)
# Homepage route

# Patients routes


