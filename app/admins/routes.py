from flask import render_template,request,url_for,redirect,session,flash,abort
from flask import Blueprint
admins=Blueprint('admins',__name__)
import os
import json
from app import db,bcrypt,mail
from app.models import *
from app.admins.forms import *
from flask_login import login_user,current_user,logout_user,login_required
import random
from app.admins.utils import *
from flask_mail import Message


# Admin routes
@admins.route("/admins/login",methods=["POST","GET"])
def adminlogin():
    form=AdminLoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('admins.admindashboard'))
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
                            return redirect(next_page) if next_page else redirect(url_for('admins.admindashboard'))
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
@admins.route("/admins/logout")
def adminlogout():
    logout_user()
    if "account_type" in session:
        session.pop('account_type',None)
    if "role" in session:
        session.pop('role',None)
    flash('You have been logged out!','success')
    return redirect(url_for("admins.adminlogin"))
@admins.route("/admins/dashboard")
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
@admins.route("/admins/manageadmins")
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

@admins.route("/admins/managepatients")
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
@admins.route("/admins/managedoctors")
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
@admins.route("/admins/doctors/new",methods=["POST","GET"])
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
                    return redirect(url_for("admins.newdoctors"))
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
@admins.route("/admins/new",methods=["POST","GET"])
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
                    return redirect(url_for("admins.newadmin"))
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
@admins.route("/admins/changepwd",methods=["POST","GET"])
@login_required
def adminchangepwd():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            form=AdminPasswordForm()
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
@admins.route("/admins/editprofile",methods=["POST","GET"])
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

@admins.route("/admins/edit/<int:user_id>",methods=["POST","GET"])
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
@admins.route("/admins/doctors/edit/<int:user_id>",methods=["POST","GET"])
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
@admins.route("/admins/patients/edit/<int:user_id>",methods=["POST","GET"])
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
                    flash('Patient Details updated successfully','success')
            return render_template('/admins/patientsedit.html',data=user,form=form, title="EDIT PATIENT'S DETAILS")
        else:
            flash('Access Denied','error')
            abort(403)
    else:
         flash('Access Denied','error')
         abort(403)



@admins.route("/admins/doctors/activate/<int:user_id>",methods=["POST","GET"])
@login_required
def adminactivatedoctor(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=DoctorCredentials.query.get_or_404(user_id)
            user.status='Activated'
            db.session.commit()
            return redirect(url_for('admins.managedoctors'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@admins.route("/admins/patients/activate/<int:user_id>",methods=["POST","GET"])
@login_required
def adminactivatepatient(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=PatientCredentials.query.get_or_404(user_id)
            user.status='Activated'
            db.session.commit()
            return redirect(url_for('admins.managepatients'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@admins.route("/admins/activate/<int:user_id>",methods=["POST","GET"])
@login_required
def adminactivateadmin(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=AdminCredentials.query.get_or_404(user_id)
            user.status='Activated'
            db.session.commit()
            return redirect(url_for('admins.manageadmins'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)

@admins.route("/admins/doctors/deactivate/<int:user_id>",methods=["POST","GET"])
@login_required
def admindeactivatedoctor(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=DoctorCredentials.query.get_or_404(user_id)
            user.status='Deactivated'
            db.session.commit()
            return redirect(url_for('admins.managedoctors'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@admins.route("/admins/patients/deactivate/<int:user_id>",methods=["POST","GET"])
@login_required
def admindeactivatepatient(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=PatientCredentials.query.get_or_404(user_id)
            user.status='Deactivated'
            db.session.commit()
            return redirect(url_for('admins.managepatients'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)
@admins.route("/admins/deactivate/<int:user_id>",methods=["POST","GET"])
@login_required
def admindeactivateadmin(user_id):
    if "account_type" in session and "role" in session:
        if session["account_type"] == "Admin" and session["role"] == "Super Admin":
            user=AdminCredentials.query.get_or_404(user_id)
            user.status='Deactivated'
            db.session.commit()
            return redirect(url_for('admins.manageadmins'))
        else:
                flash('Access Denied', 'error')
                abort(403)
    else:
        flash('Access Denied', 'error')
        abort(403)