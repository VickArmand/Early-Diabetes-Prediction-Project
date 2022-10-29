from flask import render_template,request,url_for,redirect,session,flash,abort,jsonify
import os
import json
import sqlite3
import io
from app import app,pk,np,db,bcrypt
from app import sendnotification
from app.models import *
from app.forms import * 
from app.modelutils import ModelUtils as mutils
from flask_login import login_user,current_user,logout_user,login_required
import random
from app.sendnotification import *
# Constructing web routes
datasetpath='./app/static/Datasets'
datasetfile= "diabetes.csv"
datasetpathfile=os.path.join(datasetpath,datasetfile)
modelspath='./app/static/ML Model'
modelfile= "diabetespredmodelusingxgboost.pkl"
modelpathfile=os.path.join(modelspath,modelfile)
# Homepage route
@app.route("/")
def index():
    return render_template('homepage.html')
# DB Backup 
@app.route("/backup")
def backupdb():
    conn = sqlite3.connect(os.path.join('./app', 'diabetespred.sqlite3'),check_same_thread=False) 
    with io.open('backupdatabase_dump.sql', 'w') as p:   
        # iterdump() function
        for line in conn.iterdump(): 
            p.write('%s\n' % line)
    print(' Backup performed successfully!')
    print(' Data Saved as backupdatabase_dump.sql')
    return redirect(url_for('index'))
    conn.close()
# DB Restore 
@app.route("/restore")
def restore():
    admin1=Admins(fname='Victor',lname='Mugechi',email='victormaina1962@gmail.com',gender='Male',dateofbirth=datetime.strptime('2005-01-10 00:00:00.000000','%Y-%m-%d %H:%M:%S.%f'),contact='+254727617870',county='Kiambu',area='Thika')
    admin2=Admins(fname='Jennifer',lname='Carson',email='jencarson@gmail.com',gender='Male',dateofbirth=datetime.strptime('2000-05-11 00:00:00.000000','%Y-%m-%d %H:%M:%S.%f'),contact='+254793835669',county='Mombasa',area='Kwale')
    admincredential1=AdminCredentials(uname='MugechiVictor',password='$2b$12$WVuU4dgH3jq5OvVp./0r2un03P77LY0wihXvLMLYyWHMz3plk4s4O',status='Activated',registeredadmin=admin1,role='Super Admin')
    admincredential2=AdminCredentials(uname='jencarson',password='$2b$12$2XGJ.FLIJEJbdS8W5FN6muPMLxW9EiH9Ra/xlqFRZkjxjtpETu9Ti',status='Activated',registeredadmin=admin2,role='General Admin')
    db.session.add(admincredential1)
    db.session.add(admincredential2)
    patient1=Patients(fname='Victor',lname='Mugechi',email='victormaina1962@gmail.com',gender='Male',dateofbirth=datetime.strptime('2005-09-11 00:00:00.000000','%Y-%m-%d %H:%M:%S.%f'),contact='+254727617870',county='Meru',area='Nchiru')
    patient2=Patients(fname='Noah',lname='Shebib',email='shebibnoah@gmail.com',gender='Male',dateofbirth=datetime.strptime('1998-02-18 00:00:00.000000','%Y-%m-%d %H:%M:%S.%f'),contact='+254727617870',county='Mombasa',area='Kwale')
    patientcredential1=PatientCredentials(uname='MugechiVictor',password='$2b$12$l/MFo11kJoRUHxABz7ixPONiwRXEiQh3O4Xg/KBcp8Hr1xM4KOQgi',status='Activated',registeredpat=patient1)
    patientcredential2=PatientCredentials(uname='shebibnoah',password='$2b$12$AP1MD9e0stZDyBhf/YyQJeSa5W8/X68tIN1JSkXufbx.jzRTRQmj2',status='Activated',registeredpat=patient2)
    db.session.add(patientcredential1)
    db.session.add(patientcredential2)
    doctor1=Doctors(fname='Kennedy',lname='Carson',email='kencarson@gmail.com',gender='Male',dateofbirth=datetime.strptime('2010-01-01 00:00:00.000000','%Y-%m-%d %H:%M:%S.%f'),contact='+254793835669',county='Mombasa',area='Kilifi')
    doctorcredential1=DoctorCredentials(uname='kencarson',password='$2b$12$TnBX15DcY2yRwe9k2TlD0uOHkfTNisl/pEmP5uqRoCjR9MoRwPMWK',specialty='Treatment',status='Activated',registereddoc=doctor1)
    db.session.add(doctorcredential1)
    db.session.commit()
    return redirect(url_for('index'))
# MSG SEND
@app.route("/sendmsg")
def sendmsg():
    sendnotification.sendtestmsg()
    return redirect(url_for('index'))
# Patients routes
@app.route("/login",methods=["POST","GET"])
def login():
    form=LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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
                            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
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
@app.route("/logout")
def logout():
    logout_user()
    if "account_type" in session:
        session.pop('account_type',None)
    flash('You have been logged out!','success')
    return redirect(url_for("login"))


@app.route("/register",methods=["POST","GET"])
# Patient Registration code
def register():
    # If patient already authenticated redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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

            return redirect(url_for('login'))
        else:
            # If there is an error during validation redirect back to registration page
            return render_template('/patients/register.html',form=form,title='PATIENT\'S REGISTRATION')
    
    return render_template('/patients/register.html',form=form,title='PATIENT\'S REGISTRATION')
@app.route("/dashboard")
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
@app.route("/changepwd",methods=["POST","GET"])
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
@app.route("/editprofile",methods=["POST","GET"])
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
@app.route("/monitorprogress")
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


# Admin routes
@app.route("/admins/login",methods=["POST","GET"])
def adminlogin():
    form=AdminLoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('admindashboard'))
    if request.method=='POST':
        if form.validate_on_submit():
            isAdmin=Admins.query.filter_by(email=form.email.data).first()
            if bool(isAdmin):
                credentials=AdminCredentials.query.filter_by(adminregistered=isAdmin.id).first()          
                if credentials.status=='Activated':
                    if bool(credentials):
                        if bcrypt.check_password_hash(credentials.password,form.password.data):
                            login_user(credentials.registeredadmin,remember=form.remember.data)
                            session['account_type'] ='Admin'
                            session['role']=credentials.role
                            next_page=request.args.get('next')
                            flash('Sign in success', 'success')
                            return redirect(next_page) if next_page else redirect(url_for('admindashboard'))
                        else:
                            flash('Incorrect Email or Password', 'error')
                    else:
                        flash('User does not exist', 'error')

                else:
                    flash('Access Denied', 'error')
                    abort(403)
            else:
                    flash('User does not exist', 'error')
    return render_template('/admins/login.html',form=form,title='ADMIN LOGIN')
@app.route("/admins/logout")
def adminlogout():
    logout_user()
    if "account_type" in session:
        session.pop('account_type',None)
    if "role" in session:
        session.pop('role',None)
    flash('You have been logged out!','success')
    return redirect(url_for("adminlogin"))
@app.route("/admins/dashboard")
@login_required
def admindashboard():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            return render_template('/admins/dashboard.html')
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
                flash('Access Denied', 'error')
                abort(403)
@app.route("/admins/manageadmins")
@login_required
def manageadmins():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            page = request.args.get('page', 1, type=int)
            userdata=AdminCredentials.query.paginate(page=page, per_page=5)
            return render_template('/admins/manageadmins.html', data=userdata, title='MANAGE ADMINS')
        else:
                    flash('Access Denied', 'error')
                    abort(403)
    else:
                flash('Access Denied', 'error')
                abort(403)

@app.route("/admins/managepatients")
@login_required
def managepatients():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            page = request.args.get('page', 1, type=int)
            userdata=PatientCredentials.query.paginate(page=page, per_page=5)
            return render_template('/admins/managepatients.html', data=userdata, title='MANAGE PATIENTS')
        else:
                    flash('Access Denied', 'error')
                    abort(403)
    else:
                flash('Access Denied', 'error')
                abort(403)
@app.route("/admins/managedoctors")
@login_required
def managedoctors():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            page = request.args.get('page', 1, type=int)
            userdata=DoctorCredentials.query.paginate(page=page, per_page=5)
            return render_template('/admins/managedoctors.html', data=userdata, title='MANAGE DOCTORS')
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
                flash('Access Denied', 'error')
                abort(403)
@app.route("/admins/doctors/new",methods=["POST","GET"])
@login_required
def newdoctors():
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            form=DoctorRegistrationForm()
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
                    doctor=Doctors(fname=form.firstname.data,lname=form.lastname.data,email=form.email.data,gender=form.gender.data,county=form.county.data,dateofbirth=form.DoB.data,contact=form.contact.data,area=form.area.data)
                    # db.session.add(doctor)
                    # db.session.commit()
                    doctorcredentials=DoctorCredentials(uname=form.username.data,password=hashed_password,specialty=form.specialty.data,registereddoc=doctor)
                    db.session.add(doctorcredentials)
                    db.session.commit()
                    # Session message
                    flash('Doctor registered successfully ','success')
                    return redirect(url_for("newdoctors"))
                else:
                    # If there is an error during validation redirect back to registration page
                    return render_template('/admins/newdoctors.html',form=form,title='DOCTORS REGISTRATION')
            return render_template('/admins/newdoctors.html',form=form,title='DOCTORS REGISTRATION')
        else:
                    flash('Access Denied', 'error')
                    abort(403)
    else:
                flash('Access Denied', 'error')
                abort(403)
@app.route("/admins/new",methods=["POST","GET"])
@login_required
def newadmin():
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            form=AdminRegistrationForm()
            if request.method=='POST':
                # If request type is post and there is no error during form validation
                agediff=datetime.now().year - datetime.strptime(str(form.DoB.data),'%Y-%m-%d').year
                if datetime.strptime(str(form.DoB.data),'%Y-%m-%d').year >= datetime.now().year:
                    flash("The date cannot be in the future!",'error')
                    
                elif agediff < 10:
                    flash("Age too low for registration.",'error')

                elif form.validate_on_submit():
                    # password encryption
                    hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                    # storing registration details in database
                    admin=Admins(fname=form.firstname.data,lname=form.lastname.data,email=form.email.data,gender=form.gender.data,county=form.county.data,dateofbirth=form.DoB.data,contact=form.contact.data,area=form.area.data)
                    # db.session.add(admin)
                    # db.session.commit()
                    admincredentials=AdminCredentials(uname=form.username.data,password=hashed_password,role=form.role.data,registeredadmin=admin)
                    db.session.add(admincredentials)
                    db.session.commit()
                    # Session message
                    flash('Admin registered successfully','success')
                    return redirect(url_for("newadmin"))
                else:
                    # If there is an error during validation redirect back to registration page
                    return render_template('/admins/newadmin.html',form=form,title='ADMIN REGISTRATION')
            return render_template('/admins/newadmin.html',form=form,title='ADMIN REGISTRATION')
        else:
            flash('Access Denied', 'error')
            abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/admins/changepwd",methods=["POST","GET"])
@login_required
def adminchangepwd():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            form=ChangePasswordForm()
            user=AdminCredentials.query.filter_by(adminregistered=current_user.id).first()
            if request.method=='POST':
                if form.validate_on_submit:
                    if bcrypt.check_password_hash(user.password,form.password.data):
                        hashed_password=bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                        user.password=hashed_password
                        db.session.commit()
                        flash('Password updated successfully','success')    
                    else:
                        flash('Incorrect password','error') 
            return render_template('/admins/changepassword.html',form=form,title='CHANGE PASSWORD')
        else:
            flash('Access Denied', 'error')
            abort(403)
    else:
            flash('Access Denied', 'error')
            abort(403)
@app.route("/admins/editprofile",methods=["POST","GET"])
@login_required
def admineditprofile():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            form=AdminUpdateForm()
            user=AdminCredentials.query.filter_by(adminregistered=current_user.id).first()
            if request.method=='GET':
                form.contact.data=user.registeredadmin.contact
                form.username.data=user.uname
                form.email.data=user.registeredadmin.email
            if request.method=='POST':
                if form.validate_on_submit:
                    user.registeredadmin.contact=form.contact.data
                    user.uname=form.username.data
                    user.registeredadmin.email=form.email.data
                    db.session.commit()
                    flash('Details updated successfully','success')   
            return render_template('/admins/editprofile.html',form=form,title='EDIT YOUR PROFILE')
        else:
            flash('Access Denied', 'error')
            abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)

@app.route("/admins/edit/<int:user_id>",methods=["POST","GET"])
@login_required
def admineditadmin(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            form=AdminEditAdmins()
            user=AdminCredentials.query.get_or_404(user_id)
            if request.method=='GET':
                form.firstname.data=user.registeredadmin.fname
                form.lastname.data=user.registeredadmin.lname
                form.area.data=user.registeredadmin.area
                form.gender.data=user.registeredadmin.gender
                form.county.data=user.registeredadmin.county
                form.DoB.data=datetime.strptime(str(user.registeredadmin.dateofbirth),'%Y-%m-%d %H:%M:%S')
                form.status.data=user.status
                form.role.data=user.role
            if request.method=='POST':
                if form.validate_on_submit:
                    user.registeredadmin.fname=form.firstname.data
                    user.registeredadmin.lname=form.lastname.data
                    user.registeredadmin.area=form.area.data
                    user.registeredadmin.gender=form.gender.data
                    user.registeredadmin.county=form.county.data
                    user.registeredadmin.dateofbirth=form.DoB.data
                    user.status=form.status.data
                    user.role=form.role.data
                    db.session.commit()
                    flash('Doctors Details updated successfully','success')
            return render_template('/admins/adminsedit.html',data=user,form=form,title="EDIT ADMIN'S DETAILS")
        else:
            flash('Access Denied','error')
            abort(403)
    else:
         flash('Access Denied','error')
         abort(403)
@app.route("/admins/doctors/edit/<int:user_id>",methods=["POST","GET"])
@login_required
def admineditdoctor(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            form=AdminEditDoctors()
            user=DoctorCredentials.query.get_or_404(user_id)
            if request.method=='GET':
                form.firstname.data=user.registereddoc.fname
                form.lastname.data=user.registereddoc.lname
                form.area.data=user.registereddoc.area
                form.gender.data=user.registereddoc.gender
                form.county.data=user.registereddoc.county
                form.DoB.data=datetime.strptime(str(user.registereddoc.dateofbirth),'%Y-%m-%d %H:%M:%S')
                form.status.data=user.status
                form.specialty.data=user.specialty
            if request.method=='POST':
                if form.validate_on_submit:
                    user.registereddoc.fname=form.firstname.data
                    user.registereddoc.lname=form.lastname.data
                    user.registereddoc.area=form.area.data
                    user.registereddoc.gender=form.gender.data
                    user.registereddoc.county=form.county.data
                    user.registereddoc.dateofbirth=form.DoB.data
                    user.status=form.status.data
                    user.specialty=form.specialty.data
                    db.session.commit()
                    flash('Doctors Details updated successfully','success')
            return render_template('/admins/doctorsedit.html',data=user,form=form,title="EDIT DOCTOR'S DETAILS")
        else:
            flash('Access Denied', 'error')
            abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/admins/patients/edit/<int:user_id>",methods=["POST","GET"])
@login_required
def admineditpatient(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            form=AdminEditPatients()
            user=PatientCredentials.query.get_or_404(user_id)
            if request.method=='GET':
                form.firstname.data=user.registeredpat.fname
                form.lastname.data=user.registeredpat.lname
                form.area.data=user.registeredpat.area
                form.gender.data=user.registeredpat.gender
                form.county.data=user.registeredpat.county
                form.DoB.data=datetime.strptime(str(user.registeredpat.dateofbirth),'%Y-%m-%d %H:%M:%S')
                form.status.data=user.status
                
            if request.method=='POST':
                if form.validate_on_submit:
                    user.registeredpat.fname=form.firstname.data
                    user.registeredpat.lname=form.lastname.data
                    user.registeredpat.area=form.area.data
                    user.registeredpat.gender=form.gender.data
                    user.registeredpat.county=form.county.data
                    user.registeredpat.dateofbirth=form.DoB.data
                    user.status=form.status.data
                    db.session.commit()
                    flash('Doctors Details updated successfully','success')
            return render_template('/admins/patientsedit.html',data=user,form=form, title="EDIT PATIENT'S DETAILS")
        else:
            flash('Access Denied','error')
            abort(403)
    else:
         flash('Access Denied','error')
         abort(403)



@app.route("/admins/doctors/activate/<int:user_id>",methods=["POST","GET"])
@login_required
def adminactivatedoctor(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=DoctorCredentials.query.get_or_404(user_id)
            user.status='Activated'
            db.session.commit()
            return redirect(url_for('managedoctors'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/admins/patients/activate/<int:user_id>",methods=["POST","GET"])
@login_required
def adminactivatepatient(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=PatientCredentials.query.get_or_404(user_id)
            user.status='Activated'
            db.session.commit()
            return redirect(url_for('managepatients'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/admins/activate/<int:user_id>",methods=["POST","GET"])
@login_required
def adminactivateadmin(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=AdminCredentials.query.get_or_404(user_id)
            user.status='Activated'
            db.session.commit()
            return redirect(url_for('manageadmins'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)

@app.route("/admins/doctors/deactivate/<int:user_id>",methods=["POST","GET"])
@login_required
def admindeactivatedoctor(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=DoctorCredentials.query.get_or_404(user_id)
            user.status='Deactivated'
            db.session.commit()
            return redirect(url_for('managedoctors'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/admins/patients/deactivate/<int:user_id>",methods=["POST","GET"])
@login_required
def admindeactivatepatient(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=PatientCredentials.query.get_or_404(user_id)
            user.status='Deactivated'
            db.session.commit()
            return redirect(url_for('managepatients'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/admins/deactivate/<int:user_id>",methods=["POST","GET"])
@login_required
def admindeactivateadmin(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=AdminCredentials.query.get_or_404(user_id)
            user.status='Deactivated'
            db.session.commit()
            return redirect(url_for('manageadmins'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
# Doctors routes
@app.route("/doctors/login",methods=["POST","GET"])
def doctorlogin():
    form=DoctorLoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('doctordashboard'))
    if request.method=='POST':
        if form.validate_on_submit():
            isDoctor=Doctors.query.filter_by(email=form.email.data).first()
            if bool(isDoctor):
                credentials=DoctorCredentials.query.filter_by(doctorregistered=isDoctor.id).first()          
                if credentials.status=='Activated':
                    if bool(credentials):
                        if bcrypt.check_password_hash(credentials.password,form.password.data):
                            login_user(credentials.registereddoc,remember=form.remember.data)
                            session['account_type'] ='Doctor'
                            session['specialty']=credentials.specialty
                            next_page=request.args.get('next')
                            flash('Sign in success', 'success')
                            return redirect(next_page) if next_page else redirect(url_for('doctordashboard'))
                        else:
                            flash('Incorrect Email or Password', 'error')
                    else:
                        flash('User does not exist', 'error')
                        abort(403)
                else:
                    flash('Access Denied', 'error')
                    abort(403)
            else:
                flash('User does not exist', 'error')
    return render_template('/doctors/login.html',form=form, title='DOCTOR\'S LOGIN')
@app.route("/doctors/logout")
def doctorlogout():
    logout_user()
    if "account_type" in session:
        session.pop('account_type',None)
    if "specialty" in session:
        session.pop('specialty',None)
    flash('You have been logged out!','success')
    return redirect(url_for("doctorlogin"))
@app.route("/doctors/dashboard")
@login_required
def doctordashboard():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            return render_template('/doctors/dashboard.html')
        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)

@app.route("/doctors/predict", methods=['POST','GET'])
@login_required
def predict():
    if "account_type" in session and "specialty" in session:
        if session["account_type"] == "Doctor" and session["specialty"] == "Treatment":
                
                form=HealthPredictionForm()
                form.patientsselect.choices=[(patient.id, " ".join([patient.fname, patient.lname])) for patient in Patients.query.all()]
                if request.method=='POST':
                    # Model loading
                    classifier=pk.load(open(modelpathfile,'rb'))
                    # Obtaining features from sliders
                    pregnanciesno=request.form["pregnancies"]
                    # if pregnanciesno == 'None':
                    #     pregnanciesno=0
                    # if pregnanciesno == 'Greater than or equal to one and less than five':
                    #     pregnanciesno=random.randint(1,5)
                    # if pregnanciesno == 'Greater than or equal to five':
                    #     pregnanciesno=random.randint(5,15)
                    glucose=request.form["glucose"]
                    if glucose == 'Less than or equal to 80 mg/dl':
                        glucose=random.randint(50,80)
                    if glucose == 'Greater than 80 mg/dl and less than or equal to 100 mg/dl':
                        glucose=random.randint(81,100)
                    if glucose == 'Greater than 100 mg/dl and less than or equal to 120 mg/dl':
                        glucose=random.randint(101,120)
                    if glucose == 'Greater than 120 mg/dl and less than or equal to 130 mg/dl':
                        glucose=random.randint(121,130)
                    if glucose == 'Greater than 130 mg/dl and less than or equal to 145 mg/dl':
                        glucose=random.randint(130,145)
                    if glucose == 'Greater than 145 mg/dl and less than or equal to 160 mg/dl':
                        glucose=random.randint(146,160)
                    if glucose == 'Greater than 160 mg/dl and less than or equal to 170 mg/dl':
                        glucose=random.randint(161,170)
                    if glucose == 'Greater than 170 mg/dl':
                        glucose=random.randint(171,200)
                    height=request.form["height"]
                    if height == 'Less than or equal to 100cm':
                        height=1.0
                    if height == 'Greater than 100cm and less than 200cm':
                        height=round(random.uniform(1.1,1.9),1)
                    if height == 'Greater than or equal to 200cm':
                        height=round(random.uniform(2.0,3.0),1)
                    weight=request.form["weight"]
                    if weight == 'Less than 50kg':
                        weight=round(random.uniform(30.0,49.9),1)
                    if weight == 'Greater than or equal to 50kg and less than 84kg':
                        weight=round(random.uniform(50.0,83.9),1)
                    if weight == 'Greater than or equal to 84kg and less than 112kg':
                        weight=round(random.uniform(84.1,111.9),1)
                    if weight == 'Greater than 112kg':
                        weight=round(random.uniform(112.0,130.0),1)
                    pedigree=request.form["pedigree"]
                    pedigreevalue=0
                    if pedigree == 'Yes':
                        pedigree=round(random.uniform(1.0,2.5),3)
                        pedigreevalue=1
                    if pedigree == 'No':
                        pedigree=round(random.uniform(0.0,1.0),3)
                        pedigreevalue=0
                    insulin=request.form["insulin"]
                    if insulin == 'Less than or equal to 20 mU/ml':
                        insulin=random.randint(10,20)
                    if insulin == 'Greater than 20 mU/ml and Less than or equal to 80 mU/ml':
                        insulin=random.randint(21,80)
                    if insulin == 'Greater than 80 mU/ml and less than or equal to 150 mU/ml':
                        insulin=random.randint(81,150)
                    if insulin == 'Greater than 150 mU/ml and less than or equal to 300 mU/ml':
                        insulin=random.randint(151,300)
                    if insulin == 'Greater than 300 mU/ml and less than or equal to 500 mU/ml':
                        insulin=random.randint(301,500)
                    if insulin == 'Greater than 500 mU/ml':
                        insulin=random.randint(501,800)
                    bmi=round(float(weight)/(float(height)**2),1)
                    patientid=int(request.form['patientsselect'])
                    patientdetails=Patients.query.filter_by(id=patientid).first()
                    patientDoB=patientdetails.dateofbirth
                    patientcontact=patientdetails.contact
                    patientdob=datetime.strptime(str(patientDoB), '%Y-%m-%d %H:%M:%S')
                    age=datetime.now().year-patientdob.year
                    features=[pregnanciesno,glucose,insulin,bmi,pedigree,age]
                    features=[float (x) for x in features]
                    features=np.array(features)
                    features=features.reshape(1,-1)
                    # outcome prediction
                    predictionvalue=classifier.predict(features)
                    predictionprob=round(classifier.predict_proba(features)[0][1]*100,2)
                    # Storing predictions in database
                    predictionresults=Predictions(glucose=glucose,pregnancies=pregnanciesno,insulin=insulin,height=height,weight=weight,pedigree=pedigreevalue,bmi=bmi,age=age,outcome=predictionvalue[0].item(),patientpred=patientid)
                    db.session.add(predictionresults)
                    db.session.commit()
                    predstr=" "
                    if predictionvalue[0].item() == 0:
                        predstr="low risk of diabetes"
                    else:
                        predstr="high risk of diabetes"
                    # send msg
                    message=f"Hello there patient {patientdetails.fname} {patientdetails.lname} , Mugema's Diabetes Prediction is here to inform you that from your recent diagosis on {datetime.now().strftime('%Y-%m-%d')} the predictions have yielded that you are at {predstr} due to the fact that you have a {predictionprob}% chance of having diabetes. Remember its important to maintain healthy weight, get regular exercise, eat a healthy diet. Thank you and together let's fight against diabetes"
                    response,issent=sendnotification.sendcustomizedsms(patientcontact,message,False)
                    if issent :
                        notifications=PatientMessages(title='Health Status Notification',body=message,recipientpat=patientdetails)
                        db.session.add(notifications)
                        db.session.commit()
                        flash("Message sent successfully to patient","success")
                    else:
                        notifications=PatientMessages(title='Health Status Notification',body=message,status='Failed',recipientpat=patientdetails)
                        db.session.add(notifications)
                        db.session.commit()
                        flash("Message sending failed","error")
                    return render_template('/doctors/predictdisease.html',pred=predictionvalue[0].item(),prob=predictionprob,form=form,title='PATIENT HEALTH PREDICTION',res=[pregnanciesno,glucose,insulin,height,weight,bmi,age,pedigree,predictionvalue[0].item()])
                else:
                    return render_template('/doctors/predictdisease.html',form=form,title='PATIENT HEALTH PREDICTION')
        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/doctors/predict/<int:patient_id>", methods=['POST','GET'])
@login_required
def predictwithid(patient_id):
    if "account_type" in session and "specialty" in session:
        if session["account_type"] == "Doctor" and session["specialty"] == "Treatment":
                patients=Patients.query.all()
                form=HealthPredictionForm()
                patient=Patients.query.get_or_404(patient_id)
                form.patientsselect.choices=[(patient.id, " ".join([patient.fname, patient.lname])) for patient in Patients.query.all()]
                form.patientsselect.default=patient_id
                form.process()
                return render_template('/doctors/predictdisease.html',patients=patients,form=form,title='PATIENT HEALTH PREDICTION')

        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/doctors/train")
@login_required
def trainmodel():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            X,Y=mutils.datapreprocessing(datasetpathfile)
            return render_template('/doctors/accuracycomputation.html',trainingresults=mutils.train(X,Y),title='ACCURACY COMPUTATION')
        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/doctors/accuracy")
@login_required
def displayaccuracypage():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            return render_template('/doctors/accuracycomputation.html',title='ACCURACY COMPUTATION')
        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/doctors/accuracyreports")
@login_required
def computemetrics():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            X,Y=mutils.datapreprocessing(datasetpathfile)
            return render_template('/doctors/accuracycomputation.html',evaluationmetrics=mutils.computemetrics(X,Y),title='ACCURACY COMPUTATION')
        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/doctors/reports")
@login_required
def doctorsreports():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            page = request.args.get('page', 1, type=int)
            patientdata=Predictions.query.paginate(page=page, per_page=5)
            return render_template('/doctors/reports.html',patients=patientdata, title='PATIENT REPORTS')
        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/doctors/fetchrecords" ,methods=['POST','GET'])
def asyncfetchrecords():
    results =""
    if request.method=='POST':
        qtc_data = request.get_json()
        if qtc_data['Gender'] and not qtc_data['Outcome']:
            records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.county, Predictions.outcome,Predictions.date_predicted).filter(Patients.gender==qtc_data['Gender']).all()
            results = {'rows': records}
        elif not qtc_data['Gender'] and qtc_data['Outcome']:
            records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.county, Predictions.outcome,Predictions.date_predicted).filter(Predictions.outcome==qtc_data['Outcome']).all()
            # records=[tuple(row) for row in records]
            results = {'rows': records}     
    #         userList = users.query\
    # .join(friendships, users.id==friendships.user_id)\
    # .add_columns(users.userId, users.name, users.email, friends.userId, friendId)\
    # .filter(users.id == friendships.friend_id)\
    # .filter(friendships.user_id == userID)\
    # .paginate(page, 1, False)
        elif qtc_data['Gender'] and qtc_data['Outcome']:
            records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.county, Predictions.outcome,Predictions.date_predicted).filter(Patients.gender==qtc_data['Gender'],Predictions.outcome==qtc_data['Outcome']).all()
            results = {'rows': records}
            
        else:
            return json.dumps(results ,default=str)
        # print (json.dumps(results ,default=str))
        return json.dumps(results ,default=str)
@app.route("/doctors/messages")
@login_required
def patientnotifications():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            page = request.args.get('page', 1, type=int)
            patientdata=PatientMessages.query.order_by(PatientMessages.date_posted.desc()).paginate(page=page, per_page=5)
            return render_template('/doctors/notifications.html',msg=patientdata, title='PATIENT NOTIFICATIONS')
        else:
            flash('Access Denied', 'error')
            abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/doctors/changepwd",methods=["POST","GET"])
@login_required
def doctorchangepwd():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            form=ChangePasswordForm()
            user=DoctorCredentials.query.filter_by(doctorregistered=current_user.id).first()
            if request.method=='POST':
                if form.validate_on_submit:
                    if bcrypt.check_password_hash(user.password,form.password.data):
                        hashed_password=bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                        user.password=hashed_password
                        db.session.commit()
                        flash('Password updated successfully','success') 
                    else:
                        flash('Incorrect password','error') 
            return render_template('/doctors/changepassword.html',form=form,title='CHANGE PASSWORD')
        else:
            flash('Access Denied', 'error')
            abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/doctors/editprofile",methods=["POST","GET"])
@login_required
def doctoreditprofile():
    if "account_type" in session and "specialty" in session:
        if session["account_type"] == "Doctor" and session["specialty"] == "Treatment":
            form=DoctorUpdateForm()
            user=DoctorCredentials.query.filter_by(doctorregistered=current_user.id).first()
            if request.method=='GET':
                form.contact.data=user.registereddoc.contact
                form.username.data=user.uname
                form.email.data=user.registereddoc.email
            if request.method=='POST':
                if form.validate_on_submit:
                    user.registereddoc.contact=form.contact.data
                    user.uname=form.username.data
                    user.registereddoc.email=form.email.data
                    db.session.commit()
                    flash('Details updated successfully','success')    
            return render_template('/doctors/editprofile.html',form=form,title='EDIT YOUR PROFILE')
        else:
            flash('Access Denied', 'error')
            abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@app.route("/doctors/patients")
@login_required
def viewpatients():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            page = request.args.get('page', 1, type=int)
            userdata=PatientCredentials.query.paginate(page=page, per_page=5)
            return render_template('/doctors/patients.html', data=userdata)
        else:
                    flash('Access Denied', 'error')
                    abort(403)
    else:
                flash('Access Denied', 'error')
                abort(403)