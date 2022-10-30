from flask import Flask,session
import numpy as np
import os
import pickle as pk
# predict,datapreprocessing,train,modelgeneration,computemetrics
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config.config import Config
session= session

db=SQLAlchemy()
mail=Mail()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='patients.login'
login_manager.login_message_category='warning'
from datetime import timedelta

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from app.main.routes import main
    from app.admins.routes import admins
    from app.doctors.routes import doctors
    from app.patients.routes import patients
    from app.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(admins)
    app.register_blueprint(doctors)
    app.register_blueprint(patients)
    app.register_blueprint(errors)
    app.permanent_session_lifetime=timedelta(hours=3)
    return app
