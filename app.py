from flask import Flask,render_template,request,url_for,redirect
import numpy as np
import pickle as pk
app=Flask(__name__)
model = pk.load(open("diabetespredmodelusingxgboost.pkl","rb"))
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
@app.route("/doctors/predict")
def predict():
    return render_template('/doctors/predictdisease.html')
@app.route('/predictions',methods=['POST'])
def predictions():
    # pass
    if request.method=='POST':
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
        prediction=model.predict(finalfeatures)
        if prediction==1:

          return render_template("diabetespred.html",pred=prediction)
        if prediction==0:

          return render_template("diabetespred.html",pred=prediction)
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