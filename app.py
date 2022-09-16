from flask import Flask,render_template,request,url_for,redirect
import numpy as np
import xgboost as xgb

app=Flask(__name__)

# Constructing web routes
@app.route("/")
def index():
    return render_template('homepage.html')
# Patients
@app.route("/login")
def login():
    return render_template('/patients/login.html')
@app.route("/logout")
def logout():
    return redirect(url_for("login"))
@app.route("/register")
def register():
    return render_template('/patients/register.html')
@app.route("/dashboard")
def dashboard():
    return render_template('/patients/dashboard.html')
@app.route("/editinfo")
def editinfo():
    return render_template('/patients/editinfo.html')
@app.route("/monitorprogress")
def monitorprogress():
    return render_template('/patients/patientprogress.html')
# Admins
@app.route("/admin/login")
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
@app.route("/admin/newdoctors")
def newdoctors():
    return render_template('/admins/newdoctors.html')
@app.route("/admin/newadmin")
def newadmin():
    return render_template('/admins/newadmin.html')
# Doctors
@app.route("/doctors/login")
def doctorlogin():
    return render_template('/doctors/login.html')
@app.route("/doctors/dashboard")
def doctordashboard():
    return render_template('/doctors/dashboard.html')
@app.route("/doctors/predict", methods=['POST','GET'])
def predict():

    if request.method=='POST':
        filename="diabetespredmodelusingxgboost.json"
        xgb_cls=xgb.XGBClassifier(learning_rate =0.0001,
 n_estimators=1000,
 max_depth=5,
 min_child_weight=1,
 gamma=0,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 nthread=4,
 scale_pos_weight=1,
 seed=27)
        xgb_cls.load_model(filename)
        # pregnanciesno=request.form["pregnanciesno"]
        # glucose=request.form["glucose"]
        # bmi=request.form["bmi"]
        # insulin=request.form["insulin"]
        # Age=request.form["Age"]
        # bloodpressure=request.form["bloodpressure"]
        # outcome=request.form["outcome"]
        # DiabetesPedigreeFunction=request.form["DiabetesPedigreeFunction"]
        # SkinThickness=request.form["SkinThickness"]
        features=[float(x) for x in request.form.values()]
        finalfeatures=[np.array(features)]
        sample1=[6,148,72,35,0,33.6,0.627,50]
        #sample1=[5,116,74,0,0,25.6,0.201,30]
        sample1=np.array(sample1)
        sample1=sample1.reshape(1,-1)
        prediction=xgb_cls.predict(sample1)
        if prediction==1:

          return render_template('/doctors/predictdisease.html',pred="You have higher chances of Diabetes")
          objectRep.close()
        if prediction==0:

          return render_template('/doctors/predictdisease.html',pred="You have minimal chances of Diabetes")
          objectRep.close()
    else:
         return render_template('/doctors/predictdisease.html')
@app.route("/doctors/accuracy")
def computeaccuracy():
    return render_template('/doctors/accuracycomputation.html')
@app.route("/doctors/reports")
def doctorsreports():
    return render_template('/doctors/reports.html')
@app.route("/doctors/messages")
def patientnotifications():
    return render_template('/doctors/notifications.html')
if __name__ == "__main__":
    app.run(debug=True)
    