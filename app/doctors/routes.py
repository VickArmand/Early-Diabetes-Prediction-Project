from flask import render_template,request,url_for,redirect,session,flash,abort
from flask import Blueprint
doctors=Blueprint('doctors',__name__)
import os
import json
from app import pk,np,db,bcrypt,mail
from app.models import *
from app.doctors.forms import *
from flask_login import login_user,current_user,logout_user,login_required
import random
from app.doctors.utils import *
from werkzeug.exceptions import BadRequestKeyError
from flask_mail import Message
datasetpath='./app/static/Datasets'
datasetfile= "diabetes.csv"
datasetpathfile=os.path.join(datasetpath,datasetfile)
modelspath='./app/static/ML Model'
modelfile= "diabetespredmodelusingxgboost.pkl"
modelpathfile=os.path.join(modelspath,modelfile)
# Doctors routes
@doctors.route("/doctors/login",methods=["POST","GET"])
def doctorlogin():
    form=DoctorLoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('doctors.doctordashboard'))
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
                            return redirect(next_page) if next_page else redirect(url_for('doctors.doctordashboard'))
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
@doctors.route("/doctors/logout")
def doctorlogout():
    logout_user()
    if "account_type" in session:
        session.pop('account_type',None)
    if "specialty" in session:
        session.pop('specialty',None)
    flash('You have been logged out!','success')
    return redirect(url_for("doctors.doctorlogin"))
@doctors.route("/doctors/dashboard")
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

@doctors.route("/doctors/predict", methods=['POST','GET'])
@login_required
def predict():
    if "account_type" in session and "specialty" in session:
        if session["account_type"] == "Doctor" and session["specialty"] == "Treatment":
                
                form=HealthPredictionForm()
                form.patientsselect.choices=[(patient.id, " ".join([patient.fname, patient.lname])) for patient in Patients.query.all()]
                if request.method=='POST':
                    # Model loading
                    patientid=int(request.form['patientsselect'])
                    pregnanciesno=request.form["pregnancies"]
                    patientdetails=Patients.query.filter_by(id=patientid).first()
                    if patientdetails.gender == 'Male' and int(pregnanciesno) != 0:
                        flash("Invalid pregnancy value for male patient",'error')
                        return render_template('/doctors/predictdisease.html',form=form,title='PATIENT HEALTH PREDICTION')
                    else:
                        classifier=pk.load(open(modelpathfile,'rb'))
                        # Obtaining features from sliders
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
                        response,issent=sendcustomizedsms(patientcontact,message,False)
                        print(response)
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
@doctors.route("/doctors/predict/<int:patient_id>", methods=['POST','GET'])
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
@doctors.route("/doctors/train")
@login_required
def trainmodel():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            X,Y=datapreprocessing(datasetpathfile)
            return render_template('/doctors/accuracycomputation.html',trainingresults=train(X,Y),title='ACCURACY COMPUTATION')
        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)
@doctors.route("/doctors/accuracy")
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
@doctors.route("/doctors/accuracyreports")
@login_required
def computemetrics():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            X,Y=datapreprocessing(datasetpathfile)
            return render_template('/doctors/accuracycomputation.html',evaluationmetrics=computemodelmetrics(X,Y),title='ACCURACY COMPUTATION')
        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)
@doctors.route("/doctors/reports")
@login_required
def doctorsreports():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            form=ReportForm()
            page = request.args.get('page', 1, type=int)
            patientdata=Predictions.query.paginate(page=page, per_page=5)
            return render_template('/doctors/reports.html',patients=patientdata,form=form, title='PATIENT REPORTS')
        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)
# @doctors.route("/doctors/fetchrecords" ,methods=['POST','GET'])
# def asyncfetchrecords():
#     results =""
#     if request.method=='POST':
#         qtc_data = request.get_json()
#         if qtc_data['Gender'] and not qtc_data['Outcome']:
#             records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.gender, Patients.county, Patients.gender, Predictions.outcome,Predictions.date_predicted).filter(Patients.gender==qtc_data['Gender']).all()
#             rows=[]  
#             results = {'rows':{}}
#             num=0
#             for record in records:
#                 results['rows'][num]=[]
#                 rows.append(record.fname +" "+record.lname)
#                 rows.append(record.contact)
#                 rows.append(record.gender)
#                 rows.append(record.county)
#                 rows.append(record.outcome)
#                 rows.append(record.date_predicted)
#                 results['rows'][num]+=rows
#                 num+=1
#                 rows.clear()

#             print(results)
#         elif not qtc_data['Gender'] and qtc_data['Outcome']:
#             records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.county, Patients.gender, Predictions.outcome,Predictions.date_predicted).filter(Predictions.outcome==qtc_data['Outcome']).all()
#             # records=[tuple(row) for row in records]
#             rows=[]  
#             results = {'rows':{}}
#             num=0
#             for record in records:
#                 results['rows'][num]=[]
#                 rows.append(record.fname +" "+record.lname)
#                 rows.append(record.contact)
#                 rows.append(record.gender)
#                 rows.append(record.county)
#                 rows.append(record.outcome)
#                 rows.append(record.date_predicted)
#                 results['rows'][num]+=rows
#                 num+=1
#                 rows.clear()

#             print(results)
            
#     #         userList = users.query\
#     # .join(friendships, users.id==friendships.user_id)\
#     # .add_columns(users.userId, users.name, users.email, friends.userId, friendId)\
#     # .filter(users.id == friendships.friend_id)\
#     # .filter(friendships.user_id == userID)\
#     # .paginate(page, 1, False)
#         elif qtc_data['Gender'] and qtc_data['Outcome']:
#             records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.gender, Patients.county, Predictions.outcome,Predictions.date_predicted).filter(Patients.gender==qtc_data['Gender'],Predictions.outcome==qtc_data['Outcome']).all()
#             rows=[]  
#             results = {'rows':{}}
#             num=0
#             for record in records:
#                 results['rows'][num]=[]
#                 rows.append(record.fname +" "+record.lname)
#                 rows.append(record.contact)
#                 rows.append(record.gender)
#                 rows.append(record.county)
#                 rows.append(record.outcome)
#                 rows.append(record.date_predicted)
#                 results['rows'][num]+=rows
#                 num+=1
#                 rows.clear()

#             print(results)
            
#         else:
#             return json.dumps(results ,default=str)
#         # print (json.dumps(results ,default=str))
#         return json.dumps(results ,default=str)
@doctors.route("/doctors/fetchrecords" ,methods=['POST','GET'])
def fetchrecords():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            form=ReportForm()
            records =[]
            if request.method=='POST':
                gender = request.form["genderselect"]
                outcome = request.form["outcomeselect"]
                county = request.form["countyselect"]
                page=""
                try:
                    page = int(request.form["paginationnum"]) if request.form["paginationnum"] else 1
                except BadRequestKeyError:
                    page=1
                
                print("sdfghj")
                if gender and not outcome and not county:
                    records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.gender, Patients.county, Patients.gender, Predictions.outcome,Predictions.date_predicted).filter(Patients.gender==gender).paginate(page=page, per_page=5)
                elif gender and outcome and not county:
                    records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.county, Patients.gender, Predictions.outcome,Predictions.date_predicted).filter(Patients.gender==gender,Predictions.outcome==outcome).paginate(page=page, per_page=5)
                elif gender and not outcome and county:
                    records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.county, Patients.gender, Predictions.outcome,Predictions.date_predicted).filter(Patients.gender==gender,Patients.county==county).paginate(page=page, per_page=5)
                elif not gender and outcome and not county:
                    records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.county, Patients.gender, Predictions.outcome,Predictions.date_predicted).filter(Predictions.outcome==outcome).paginate(page=page, per_page=5)
                elif not gender and outcome and county:
                    records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.county, Patients.gender, Predictions.outcome,Predictions.date_predicted).filter(Predictions.outcome==outcome, Patients.county==county).paginate(page=page, per_page=5)
                elif not gender and not outcome and county:
                    records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.county, Patients.gender, Predictions.outcome,Predictions.date_predicted).filter(Patients.county==county).paginate(page=page, per_page=5)
            #         userList = users.query\
            # .join(friendships, users.id==friendships.user_id)\
            # .add_columns(users.userId, users.name, users.email, friends.userId, friendId)\
            # .filter(users.id == friendships.friend_id)\
            # .filter(friendships.user_id == userID)\
            # .paginate(page, 1, False)
                elif gender and outcome and county:
                    records=Predictions.query.join(Patients, Patients.id==Predictions.patientpred).add_columns(Patients.fname, Patients.lname, Patients.contact, Patients.gender, Patients.county, Predictions.outcome,Predictions.date_predicted).filter(Patients.gender==gender,Predictions.outcome==outcome,Patients.county==county).paginate(page=page, per_page=5)
                    
                else:
                    return render_template('/doctors/reportsanalysis.html',filteredpatients=records, form=form, title='PATIENT REPORTS')
            return render_template('/doctors/reportsanalysis.html',filteredpatients=records, form=form, title='PATIENT REPORTS')
        else:
            flash('Access Denied', 'error')
            abort(403)

    else:
        flash('Access Denied', 'error')
        abort(403)
@doctors.route("/doctors/messages")
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
@doctors.route("/doctors/changepwd",methods=["POST","GET"])
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
@doctors.route("/doctors/editprofile",methods=["POST","GET"])
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
@doctors.route("/doctors/patients")
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
@doctors.route("/doctors/predictions")
@login_required
def viewpredictions():
    if "account_type" in session:
        if session["account_type"] == "Doctor":
            page = request.args.get('page', 1, type=int)
            userdata=Predictions.query.paginate(page=page, per_page=5)
            return render_template('/doctors/predictions.html', data=userdata)
        else:
                    flash('Access Denied', 'error')
                    abort(403)
    else:
                flash('Access Denied', 'error')
                abort(403)