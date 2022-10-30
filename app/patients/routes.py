from flask import render_template,request,url_for,redirect,session,flash,abort
import os
import json
from app import db,bcrypt,mail
from app.models import *
from app.patients.forms import *
from flask_login import login_user,current_user,logout_user,login_required
import random
from app.patients.utils import *
from flask_mail import Message
from flask import Blueprint
patients=Blueprint('patients',__name__)

@patients.route("/login",methods=["POST","GET"])
def login():
    form=LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('patients.dashboard'))
    if request.method=='POST':
        if form.validate_on_submit():
            isPatient=Patients.query.filter_by(email=form.email.data).first()
            if bool(isPatient):
                credentials=PatientCredentials.query.filter_by(patientregistered=isPatient.id).first()            
                if credentials.status=='Activated':
                    if bool(credentials):
                        if bcrypt.check_password_hash(credentials.password,form.password.data):
                            login_user(credentials.registeredpat,remember=form.remember.data)
                            session['account_type'] ='Patient'
                            next_page=request.args.get('next')
                            flash('Sign in success', 'success')
                            return redirect(next_page) if next_page else redirect(url_for('patients.dashboard'))
                        else:
                            flash('Incorrect Email or Password', 'error')
                    else:
                        flash('User does not exist', 'error')
                else:
                    flash('Access Denied', 'error')
                    abort(403)
            else:
                flash('User does not exist', 'error')
    return render_template('/patients/login.html',form=form, title='PATIENT\'S SIGN IN')
@patients.route("/logout")
def logout():
    logout_user()
    if "account_type" in session:
        session.pop('account_type',None)
    flash('You have been logged out!','success')
    return redirect(url_for("patients.login"))


@patients.route("/register",methods=["POST","GET"])
# Patient Registration code
def register():
    # If patient already authenticated redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('patients.dashboard'))
    form=RegistrationForm()
    if request.method=='POST':
        agediff=datetime.now().year - datetime.strptime(str(form.DoB.data),'%Y-%m-%d').year
        # If request type is post and there is no error during form validation
        if datetime.strptime(str(form.DoB.data),'%Y-%m-%d').year >= datetime.now().year:
            flash("The date cannot be in the future!",'error')
        
        elif agediff < 10:
            flash("Age too low for registration.",'error')
        elif form.validate_on_submit():
            # password encryption
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # storing registration details in database
            patient=Patients(fname=form.firstname.data,lname=form.lastname.data,email=form.email.data,gender=form.gender.data,county=form.county.data,dateofbirth=form.DoB.data,contact=form.contact.data,area=form.area.data)
            # db.session.add(patient)
            # db.session.commit()
            
            patientcredentials=PatientCredentials(uname=form.username.data,password=hashed_password,registeredpat=patient)
            db.session.add(patientcredentials)
            db.session.commit()
            # Session message
            flash('Your account has been created. You are now able to login ','success')

            return redirect(url_for('patients.login'))
        else:
            # If there is an error during validation redirect back to registration page
            return render_template('/patients/register.html',form=form,title='PATIENT\'S REGISTRATION')
    
    return render_template('/patients/register.html',form=form,title='PATIENT\'S REGISTRATION')
@patients.route("/dashboard")
@login_required
def dashboard():
    if "account_type" in session:
        if session["account_type"] == "Patient":
            return render_template('/patients/dashboard.html')
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
                flash('Access Denied', 'error')
                abort(403)
@patients.route("/changepwd",methods=["POST","GET"])
@login_required
def changepwd():     
    if "account_type" in session:
        if session["account_type"] == "Patient":
            form=ChangePasswordForm()
            user=PatientCredentials.query.filter_by(patientregistered=current_user.id).first()
            if request.method=='POST':
                if form.validate_on_submit:
                    if bcrypt.check_password_hash(user.password,form.password.data):
                        hashed_password=bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                        user.password=hashed_password
                        db.session.commit()
                        flash('Password updated successfully','success')
                    else:
                        flash('Incorrect password','error') 
            return render_template('/patients/changepassword.html',form=form,title='CHANGE PASSWORD')
        else:
            flash('Access Denied', 'error')
            abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@patients.route("/editprofile",methods=["POST","GET"])
@login_required
def editprofile():
    if "account_type" in session:
        if session["account_type"] == "Patient":
            form=UpdateForm()
            user=PatientCredentials.query.filter_by(patientregistered=current_user.id).first()
            if request.method=='GET':
                form.contact.data=user.registeredpat.contact
                form.username.data=user.uname
                form.email.data=user.registeredpat.email
            if request.method=='POST':
                if form.validate_on_submit:
                    user.registeredpat.contact=form.contact.data
                    user.uname=form.username.data
                    user.registeredpat.email=form.email.data
                    db.session.commit()
                    flash('Details updated successfully','success') 
            return render_template('/patients/editprofile.html',form=form,title='EDIT YOUR PROFILE')
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
                flash('Access Denied', 'error')
                abort(403)
@patients.route("/monitorprogress")
@login_required
def monitorprogress():
    if "account_type" in session:
        if session["account_type"] == "Patient":
            page = request.args.get('page', 1, type=int)
            patientdata=Predictions.query.filter_by(patientpred=current_user.id).order_by(Predictions.date_predicted.desc()).paginate(page=page, per_page=5)
            return render_template('/patients/patientprogress.html',patients=patientdata)
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
                flash('Access Denied', 'error')
                abort(403)

@patients.route("/resetpwd",methods=['GET','POST'])
def reset_request():
    form=RequestResetForm()
    if request.method=='POST':
        if form.validate_on_submit:
            user=Patients.query.filter_by(email=form.email.data).first()
            send_reset_mail(user)
            flash('An email has been sent with instructions to reset your password','success')
            return redirect(url_for('patients.login'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('patients.dashboard'))
        else:
            
            return render_template('patients/resetrequest.html',title='RESET PASSWORD',form=form)
        

@patients.route("/resetpwd/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('patients.dashboard'))
    user=Patients.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token')
        return redirect(url_for('patients.reset_request'))
    form= ResetPasswordForm()
    if form.validate_on_submit:
        hashed_password=bcrypt.generate_password_hash(form.password.data)
        user.password=hashed_password
        db.session.commit()
        flash('Your password has been reset','success')
        return redirect(url_for('patients.login'))
    return render_template('resettoken.html',title='RESET PASSWORD',form=form)