from flask import Flask,render_template,request,url_for,redirect
import numpy as np
import xgboost as xgb
import os
from modelutils import predict,datapreprocessing,train,modelgeneration,computemetrics
from sendnotification import sendmail
app=Flask(__name__)
diabetesdataurl='diabetes.csv'
datasetpath='./static/Datasets'
datasetfile= "diabetespredmodelusingxgboost.json"
datasetpathfile=os.path.join(datasetpath,datasetfile)
# Constructing web routes
@app.route("/")
def index():
    return render_template('homepage.html')
# Patients
@app.route("/login",methods=["POST","GET"])
def login():
    return render_template('/patients/login.html')
@app.route("/logout")
def logout():
    return redirect(url_for("login"))
@app.route("/register",methods=["POST","GET"])
def register():
    return render_template('/patients/register.html')
@app.route("/dashboard")
def dashboard():
    return render_template('/patients/dashboard.html')
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
        predictionvalue=predict()
        if predictionvalue==1:

          return render_template('/doctors/predictdisease.html',pred="You have higher chances of Diabetes")
        #   objectRep.close()
        if predictionvalue==0:

          return render_template('/doctors/predictdisease.html',pred="You have minimal chances of Diabetes")
        #   objectRep.close()
    else:
         return render_template('/doctors/predictdisease.html')
@app.route("/doctors/accuracy")
def computeaccuracy():
    X,Y=datapreprocessing(datasetpathfile)
    return render_template('/doctors/accuracycomputation.html',metrics=computemetrics(X,Y))
@app.route("/doctors/reports")
def doctorsreports():
    return render_template('/doctors/reports.html')
@app.route("/doctors/messages")
def patientnotifications():
    return render_template('/doctors/notifications.html')
if __name__ == "__main__":
    app.run(debug=True)
    