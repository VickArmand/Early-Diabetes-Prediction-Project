from flask import Flask,render_template,request,url_for,redirect,session,flash
import numpy as np
import xgboost as xgb
import os
import pickle as pk
from modelutils import ModelUtils as mutils
# predict,datapreprocessing,train,modelgeneration,computemetrics
from sendnotification import sendmail
from datetime import timedelta
app=Flask(__name__)
app.permanent_session_lifetime=timedelta(hours=3)
app.secret_key='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
datasetpath='./static/Datasets'
datasetfile= "diabetes.csv"
datasetpathfile=os.path.join(datasetpath,datasetfile)
modelspath='./static/ML Model'
modelfile= "diabetespredmodelusingxgboost.pkl"
modelpathfile=os.path.join(modelspath,modelfile)
# Constructing web routes
@app.route("/")
def index():
    return render_template('homepage.html')
# Patients
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=='POST':
        session.permanent=True
        user=request.form['username']
        session['user']=user
        flash(f'Login successful welcome {user}')
        return redirect(url_for('dashboard'))
    else: 
        if 'user' in session:
            flash('Already logged in')
            return redirect(url_for('dashboard'))  
        return render_template('/patients/login.html')
@app.route("/logout")
def logout():
    if 'user' in session:
        user=session['user']    
        flash('You have been logged out!','info')
    session.pop('user',None)
    return redirect(url_for("login"))
@app.route("/register",methods=["POST","GET"])
def register():
    return render_template('/patients/register.html')
@app.route("/dashboard")
def dashboard():
    if 'user' in session:
        user=session['user']
        return render_template('/patients/dashboard.html',user=user)
    else:
        flash('You are not logged in')
        return redirect(url_for('login'))
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
@app.route("/admin/newadmin")
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
    return render_template('/doctors/reports.html')
@app.route("/doctors/messages")
def patientnotifications():
    return render_template('/doctors/notifications.html')
if __name__ == "__main__":
    app.run(debug=True)
    