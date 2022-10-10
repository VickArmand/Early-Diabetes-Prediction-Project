from flask import render_template,request,url_for,redirect,session,flash
import os
from app import app,xgb,pk,np,db,bcrypt
from app.models import *
from app.forms import * 
from app.modelutils import ModelUtils as mutils
from flask_login import login_user,current_user,logout_user,login_required

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
            else:
                flash('User does not exist', 'error')
    return render_template('/patients/login.html',form=form)
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
            return render_template('/patients/register.html',form=form,title='PATIENT REGISTRATION')
    
    return render_template('/patients/register.html',form=form,title='PATIENT REGISTRATION')
@app.route("/dashboard")
@login_required
def dashboard():
    if "account_type" in session:
        if session["account_type"] == "Patient":
            return render_template('/patients/dashboard.html')
        else:
                flash('Access Denied', 'error')
                return redirect(url_for('login'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('login'))
@app.route("/changepwd",methods=["POST","GET"])
@login_required
def changepwd():     
    if "account_type" in session:
        if session["account_type"] == "Patient":
            form=ChangePasswordForm()
            if request.method=='POST':
                    pass
            return render_template('/patients/changepassword.html',form=form)
        else:
                flash('Access Denied', 'error')
                return redirect(url_for('login'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('login'))
@app.route("/editinfo",methods=["POST","GET"])
@login_required
def editinfo():
    if "account_type" in session:
        if session["account_type"] == "Patient":
            form=UpdateForm()
            if request.method=='POST':
                pass    
            return render_template('/patients/editinfo.html',form=form)
        else:
                flash('Access Denied', 'error')
                return redirect(url_for('login'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('login'))
@app.route("/monitorprogress")
@login_required
def monitorprogress():
    if "account_type" in session:
        if session["account_type"] == "Patient":
                return render_template('/patients/patientprogress.html')
        else:
                flash('Access Denied', 'error')
                return redirect(url_for('login'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('login'))


# Admin routes
@app.route("/admins/login",methods=["POST","GET"])
def adminlogin():
    form=LoginForm()
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
                            next_page=request.args.get('next')
                            flash('Sign in success', 'success')
                            return redirect(next_page) if next_page else redirect(url_for('admindashboard'))
                        else:
                            flash('Incorrect Email or Password', 'error')
                    else:
                        flash('User does not exist', 'error')

                else:
                    flash('Access Denied', 'error')
            else:
                    flash('User does not exist', 'error')
    return render_template('/admins/login.html',form=form)
@app.route("/admins/logout")
def adminlogout():
    logout_user()
    if "account_type" in session:
        session.pop('account_type',None)
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
                return redirect(url_for('adminlogin'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('adminlogin'))
@app.route("/admins/manageadmins")
@login_required
def manageadmins():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            return render_template('/admins/manageadmins.html')
        else:
                    flash('Access Denied', 'error')
                    return redirect(url_for('adminlogin'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('adminlogin'))
@app.route("/admins/managedoctors")
@login_required
def managedoctors():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            return render_template('/admins/managedoctors.html')
        else:
                flash('Access Denied', 'error')
                return redirect(url_for('adminlogin'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('adminlogin'))
@app.route("/admins/doctors/new",methods=["POST","GET"])
@login_required
def newdoctors():
    if "account_type" in session:
        if session["account_type"] == "Admin":
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
                    doctorcredentials=DoctorCredentials(uname=form.username.data,password=hashed_password,speciality=form.specialty.data,registereddoc=doctor)
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
                    return redirect(url_for('adminlogin'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('adminlogin'))
@app.route("/admins/new",methods=["POST","GET"])
@login_required
def newadmin():
    if "account_type" in session:
        if session["account_type"] == "Admin":
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
            else:
                return render_template('/admins/newadmin.html',form=form,title='ADMIN REGISTRATION')
        else:
                    flash('Access Denied', 'error')
                    return redirect(url_for('adminlogin'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('adminlogin'))
@app.route("/admins/changepwd",methods=["POST","GET"])
@login_required
def adminchangepwd():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            form=ChangePasswordForm()
            # if request.method=='POST':
            #     pass    

            return render_template('/admins/changepassword.html',form=form)
        else:
            flash('Access Denied', 'error')
            return redirect(url_for('adminlogin'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('adminlogin'))
@app.route("/admins/editinfo",methods=["POST","GET"])
@login_required
def admineditinfo():
    if "account_type" in session:
        if session["account_type"] == "Admin":
            form=UpdateForm()
            if request.method=='POST':
                pass    
            return render_template('/admins/editinfo.html',form=form)
        else:
            flash('Access Denied', 'error')
            return redirect(url_for('adminlogin'))
    else:
                flash('Access Denied', 'error')
                return redirect(url_for('adminlogin'))

# Doctors routes
@app.route("/doctors/login",methods=["POST","GET"])
def doctorlogin():
    form=LoginForm()
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
                            next_page=request.args.get('next')
                            flash('Sign in success', 'success')
                            return redirect(next_page) if next_page else redirect(url_for('doctordashboard'))
                        else:
                            flash('Incorrect Email or Password', 'error')
                    else:
                        flash('User does not exist', 'error')
                else:
                    flash('Access Denied', 'error')
            else:
                flash('User does not exist', 'error')
    return render_template('/doctors/login.html',form=form)
@app.route("/doctors/logout")
def doctorlogout():
    logout_user()
    if "account_type" in session:
        session.pop('account_type',None)
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
            return redirect(url_for("doctorlogin"))

    else:
        flash('Access Denied', 'error')
        return redirect(url_for("doctorlogin"))
@app.route("/doctors/predict", methods=['POST','GET'])
@login_required
def predict():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            if request.method=='POST':
                # Model loading
                classifier=pk.load(open(modelpathfile,'rb'))
                # Obtaining features from sliders
                pregnanciesno=request.form["pregnanciesno"]
                glucose=request.form["glucoselevels"]
                height=request.form["height"]
                weight=request.form["weight"]
                bmi=float(weight)/(float(height)**2)
                insulin=request.form["insulinlevels"]
                Age=request.form["age"]
                patientid=int(request.form['patientid'])
                pedigree=request.form["Pedigree"]
                SkinThickness=request.form["skinthickness"]
                features=[pregnanciesno,glucose,SkinThickness,insulin,bmi,pedigree,Age]
                features=[float (x) for x in features]
                features=np.array(features)
                features=features.reshape(1,-1)
                # outcome prediction
                predictionvalue=classifier.predict(features)
                patientDoB=Patients.query.filter_by(id=patientid).first().dateofbirth
                patientdob=datetime.strptime(patientDoB,'%Y-%m-%d')
                age=datetime.now().year-patientdob.year
                # Storing predictions in database
                predictionresults=Predictions(glucose=glucose,insulin=insulin,bmi=bmi,age=age,outcome=predictionvalue[0],patientpred=patientid)
                db.session.add(predictionresults)
                db.session.commit()
                if predictionvalue==1:
                    return render_template('/doctors/predictdisease.html',pred="You have higher chances of Diabetes")
                if predictionvalue==0:
                    return render_template('/doctors/predictdisease.html',pred="You have minimal chances of Diabetes")
            else:
                return render_template('/doctors/predictdisease.html')
                        # features=[6,148,72,35,0,33.6,50]
                # bloodpressure=request.form["pressurelevels"]
        else:
            flash('Access Denied', 'error')
            return redirect(url_for("doctorlogin"))

    else:
        flash('Access Denied', 'error')
        return redirect(url_for("doctorlogin"))
@app.route("/doctors/train")
@login_required
def trainmodel():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            X,Y=mutils.datapreprocessing(datasetpathfile)
            mutils.train(X,Y)
            return render_template('/doctors/accuracycomputation.html',metrics=[])
        else:
            flash('Access Denied', 'error')
            return redirect(url_for("doctorlogin"))

    else:
        flash('Access Denied', 'error')
        return redirect(url_for("doctorlogin"))
@app.route("/doctors/accuracy")
@login_required
def computeaccuracy():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            X,Y=mutils.datapreprocessing(datasetpathfile)
            return render_template('/doctors/accuracycomputation.html',metrics=mutils.computemetrics(X,Y))
        else:
            flash('Access Denied', 'error')
            return redirect(url_for("doctorlogin"))

    else:
        flash('Access Denied', 'error')
        return redirect(url_for("doctorlogin"))
@app.route("/doctors/reports")
@login_required
def doctorsreports():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            return render_template('/doctors/reports.html',patients=Patients.query.all())
        else:
            flash('Access Denied', 'error')
            return redirect(url_for("doctorlogin"))

    else:
        flash('Access Denied', 'error')
        return redirect(url_for("doctorlogin"))
@app.route("/doctors/messages")
@login_required
def patientnotifications():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            return render_template('/doctors/notifications.html')
        else:
            flash('Access Denied', 'error')
            return redirect(url_for("doctorlogin"))
    else:
        flash('Access Denied', 'error')
        return redirect(url_for("doctorlogin"))
@app.route("/doctors/changepwd",methods=["POST","GET"])
@login_required
def doctorchangepwd():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            form=ChangePasswordForm()
            # if request.method=='POST':
            #     pass    

            return render_template('/admins/changepassword.html',form=form)
        else:
            flash('Access Denied', 'error')
            return redirect(url_for("doctorlogin"))
    else:
        flash('Access Denied', 'error')
        return redirect(url_for("doctorlogin"))
@app.route("/doctors/editinfo",methods=["POST","GET"])
@login_required
def doctoreditinfo():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            form=UpdateForm()
            if request.method=='POST':
                pass    
            return render_template('/admins/editinfo.html',form=form)
        else:
            flash('Access Denied', 'error')
            return redirect(url_for("doctorlogin"))
    else:
        flash('Access Denied', 'error')
        return redirect(url_for("doctorlogin"))