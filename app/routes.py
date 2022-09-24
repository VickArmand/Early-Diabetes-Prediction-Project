from flask import render_template,request,url_for,redirect,session,flash
import os
from app import app,xgb,pk,np,db
from app.models import *
from app.forms import * 
from app.modelutils import ModelUtils as mutils

# Constructing web routes
datasetpath='./static/Datasets'
datasetfile= "diabetes.csv"
datasetpathfile=os.path.join(datasetpath,datasetfile)
modelspath='./static/ML Model'
modelfile= "diabetespredmodelusingxgboost.pkl"
modelpathfile=os.path.join(modelspath,modelfile)
@app.route("/")
def index():
    return render_template('homepage.html')
# Patients
@app.route("/login",methods=["POST","GET"])
def login():
    form=LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            return redirect(url_for('dashboard'))
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
       
    return render_template('/patients/login.html',form=form)
@app.route("/logout")
def logout():
    if 'patient' in session:
        user=session['patient']    
        flash('You have been logged out!','success')
    session.pop('patient',None)
    return redirect(url_for("login"))
@app.route("/register",methods=["POST","GET"])
def register():
    if request.method=='POST':
        email=request.form['email']
        fname=request.form['firstname']
        lname=request.form['lastname']
        gender=request.form['gender']
        dateofbirth=request.form['DoB']
        contact=request.form['contact']
        county=request.form['county']
        area=request.form['residentialarea']
        uname=request.form['username']
        password=request.form['password']
        confirmpassword=request.form['passwordconfirm']
        patient=Patients(db,fname,lname,email,password,gender,dateofbirth,contact,county,area,uname)
        db.session.add(patient)
        db.session.commit()
        return render_template('/patients/register.html')
    else:
        form=RegistrationForm()
        return render_template('/patients/register.html',form=form)
@app.route("/dashboard")
def dashboard():
    # if 'patient' in session:
    #     user=session['patient']
    #     return render_template('/patients/dashboard.html',user=user)
    # else:
    #     flash('You are not logged in','warning')
    #     return redirect(url_for('login'))
    return render_template('/patients/dashboard.html',user=[])

@app.route("/editinfo",methods=["POST","GET"])
def editinfo():
    return render_template('/patients/editinfo.html')
@app.route("/monitorprogress")
def monitorprogress():
    return render_template('/patients/patientprogress.html')
# Admins
@app.route("/admin/login",methods=["POST","GET"])
def adminlogin():
    return render_template('/admins/login.html')
@app.route("/admin/dashboard")
def admindashboard():
    return render_template('/admins/dashboard.html')
@app.route("/admin/manageadmins")
def manageadmins():
    return render_template('/admins/manageadmins.html')
@app.route("/admin/managedoctors")
def managedoctors():
    return render_template('/admins/managedoctors.html')
@app.route("/admin/newdoctors",methods=["POST","GET"])
def newdoctors():
    return render_template('/admins/newdoctors.html')
@app.route("/admin/newadmin",methods=["POST","GET"])
def newadmin():
    return render_template('/admins/newadmin.html')
# Doctors
@app.route("/doctors/login",methods=["POST","GET"])
def doctorlogin():
    return render_template('/doctors/login.html')
@app.route("/doctors/dashboard")
def doctordashboard():
    return render_template('/doctors/dashboard.html')
@app.route("/doctors/predict", methods=['POST','GET'])
def predict():
    if request.method=='POST':
        classifier=pk.load(open(modelpathfile,'rb'))
        pregnanciesno=request.form["pregnanciesno"]
        glucose=request.form["glucoselevels"]
        height=request.form["height"]
        weight=request.form["weight"]
        bmi=float(weight)/(float(height)**2)
        insulin=request.form["insulinlevels"]
        Age=request.form["age"]
        # bloodpressure=request.form["pressurelevels"]
        pedigree=request.form["Pedigree"]
        SkinThickness=request.form["skinthickness"]
        features=[pregnanciesno,glucose,SkinThickness,insulin,bmi,pedigree,Age]
        features=[float (x) for x in features]
        # features=[6,148,72,35,0,33.6,50]
        features=np.array(features)
        features=features.reshape(1,-1)
        predictionvalue=classifier.predict(features)
        if predictionvalue==1:

          return render_template('/doctors/predictdisease.html',pred="You have higher chances of Diabetes")
        #   objectRep.close()
        if predictionvalue==0:

          return render_template('/doctors/predictdisease.html',pred="You have minimal chances of Diabetes")
        #   objectRep.close()
    else:
         return render_template('/doctors/predictdisease.html')
@app.route("/doctors/train")
def trainmodel():
    X,Y=mutils.datapreprocessing(datasetpathfile)
    return render_template('/doctors/accuracycomputation.html',metrics=mutils.train(X,Y))
@app.route("/doctors/accuracy")
def computeaccuracy():
    X,Y=mutils.datapreprocessing(datasetpathfile)
    return render_template('/doctors/accuracycomputation.html',metrics=mutils.computemetrics(X,Y))
@app.route("/doctors/reports")
def doctorsreports():
    return render_template('/doctors/reports.html',patients=Patients.query.all())
@app.route("/doctors/messages")
def patientnotifications():
    return render_template('/doctors/notifications.html')