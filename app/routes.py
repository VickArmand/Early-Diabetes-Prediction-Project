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
            # patientemail=form.email.data
        # isAPatient=PatientCredentials.query.filter_by(id=patientemail).first()
        # if isAPatient:
        #     session.permanent=True
        #     session['patient']=patientemail
        #     session['patientid']=isAPatient.id
        #     flash(f'Login successful welcome {patientemail}','success')
        # else:
        #     flash("Patient doesn't exist",'warning')

        # return redirect(url_for('dashboard'))
    # else:   
    #     if 'patient' in session:
    #         flash('Already logged in','success')
    #         return redirect(url_for('dashboard'))
    form=LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method=='POST':
        if form.validate_on_submit():
            isPatient=Patients.query.filter_by(email=form.email.data).first()
            isActivePatient=[]
            credentials=PatientCredentials.query.filter_by(patientid=isPatient.id).first()
            isActivePatient.append(credentials.uname)
            isActivePatient.append(isPatient.email)            
            # allPatients=db.session.query(Patients,PatientCredentials).join(PatientCredentials).all()
            # isActivePatient=filter(allPatients[0][0].email==form.email.data).filter(allPatients[0][1].status=='Activated').all()
            # for pat,patc in allPatients:
            #     if patc.status=="Activated":
            #         isActivePatient.append(pat)
            #         isActivePatient.append(patc)
            # isActivePatient=allPatients.filter(allPatients.email==form.email.data,allPatients.status=='Activated').all()
            if credentials.status=='Activated':
                if bool(isActivePatient):
                    if bcrypt.check_password_hash(credentials.password,form.password.data):
                        login_user(isPatient,remember=form.remember.data)
                        next_page=request.args.get('next')
                        flash('Sign in success', 'success')
                        return redirect(next_page) if next_page else redirect(url_for('dashboard'))
                    else:
                        flash('Incorrect Email or Password', 'error')
                else:
                      flash('User does not exist', 'error')

            else:
                flash('Access Denied', 'error')
    return render_template('/patients/login.html',form=form)
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
    # if 'patient' in session:
    #     user=session['patient']    
    #     flash('You have been logged out!','success')
    # session.pop('patient',None)
@app.route("/register",methods=["POST","GET"])
# Patient Registration code
def register():
    # If patient already authenticated redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form=RegistrationForm()
    if request.method=='POST':
        # If request type is post and there is no error during form validation
        if form.validate_on_submit():
            # password encryption
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # storing registration details in database
            patient=Patients(fname=form.firstname.data,lname=form.lastname.data,email=form.email.data,gender=form.gender.data,county=form.county.data,dateofbirth=form.DoB.data,contact=form.contact.data,area=form.area.data)
            db.session.add(patient)
            db.session.commit()
            patientcredentials=PatientCredentials(uname=form.username.data,password=hashed_password,patientregistered=patient.id)
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
    # if 'patient' in session:
    #     user=session['patient']
    #     return render_template('/patients/dashboard.html',user=user)
    # else:
    #     flash('You are not logged in','warning')
    #     return redirect(url_for('login'))
    return render_template('/patients/dashboard.html')
@app.route("/changepwd",methods=["POST","GET"])
# @login_required
def changepwd():
    form=ChangePasswordForm()
    # if request.method=='POST':
    #     pass    

    return render_template('/patients/changepassword.html',form=form)
@app.route("/editinfo",methods=["POST","GET"])
# @login_required
def editinfo():
    form=UpdateForm()
    if request.method=='POST':
        pass    
    return render_template('/patients/editinfo.html',form=form)
@app.route("/monitorprogress")
@login_required
def monitorprogress():
    return render_template('/patients/patientprogress.html')


# Admin routes
@app.route("/admin/login",methods=["POST","GET"])
def adminlogin():
    return render_template('/admins/login.html')
@app.route("/admin/dashboard")
@login_required
def admindashboard():
    return render_template('/admins/dashboard.html')
@app.route("/admin/manageadmins")
@login_required
def manageadmins():
    return render_template('/admins/manageadmins.html')
@app.route("/admin/managedoctors")
@login_required
def managedoctors():
    return render_template('/admins/managedoctors.html')
@app.route("/admin/newdoctors",methods=["POST","GET"])
@login_required
def newdoctors():
    return render_template('/admins/newdoctors.html')
@app.route("/admin/newadmin",methods=["POST","GET"])
@login_required
def newadmin():
    return render_template('/admins/newadmin.html')
@app.route("/admins/changepwd",methods=["POST","GET"])
# @login_required
def adminchangepwd():
    form=ChangePasswordForm()
    # if request.method=='POST':
    #     pass    

    return render_template('/admins/changepassword.html',form=form)
@app.route("/admins/editinfo",methods=["POST","GET"])
# @login_required
def admineditinfo():
    form=UpdateForm()
    if request.method=='POST':
        pass    
    return render_template('/admins/editinfo.html',form=form)

# Doctors routes
@app.route("/doctors/login",methods=["POST","GET"])
def doctorlogin():
    return render_template('/doctors/login.html')
@app.route("/doctors/dashboard")
@login_required
def doctordashboard():
    return render_template('/doctors/dashboard.html')
@app.route("/doctors/predict", methods=['POST','GET'])
# @login_required
def predict():
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
          return render_template('/doctors/predictdisease.html',pred="You have higher chances of Diabetes",patients=Patients.query.all())
        if predictionvalue==0:
          return render_template('/doctors/predictdisease.html',pred="You have minimal chances of Diabetes",patients=Patients.query.all())
    else:
         return render_template('/doctors/predictdisease.html',patients=Patients.query.all())
                 # features=[6,148,72,35,0,33.6,50]
        # bloodpressure=request.form["pressurelevels"]
@app.route("/doctors/train")
# @login_required
def trainmodel():
    X,Y=mutils.datapreprocessing(datasetpathfile)
    mutils.train(X,Y)
    return render_template('/doctors/accuracycomputation.html',metrics=[])
@app.route("/doctors/accuracy")
# @login_required
def computeaccuracy():
    X,Y=mutils.datapreprocessing(datasetpathfile)
    return render_template('/doctors/accuracycomputation.html',metrics=mutils.computemetrics(X,Y))
@app.route("/doctors/reports")
# @login_required
def doctorsreports():
    return render_template('/doctors/reports.html',patients=Patients.query.all())
@app.route("/doctors/messages")
@login_required
def patientnotifications():
    return render_template('/doctors/notifications.html')
@app.route("/doctors/changepwd",methods=["POST","GET"])
# @login_required
def doctorchangepwd():
    form=ChangePasswordForm()
    # if request.method=='POST':
    #     pass    

    return render_template('/admins/changepassword.html',form=form)
@app.route("/doctors/editinfo",methods=["POST","GET"])
# @login_required
def doctoreditinfo():
    form=UpdateForm()
    if request.method=='POST':
        pass    
    return render_template('/admins/editinfo.html',form=form)