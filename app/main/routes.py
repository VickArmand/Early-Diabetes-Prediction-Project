from flask import Blueprint
from flask import render_template,request,url_for,redirect,session,flash,abort,jsonify
import os
import sqlite3
import io
from app.main.utils import sendtestmsg
from app.models import *
main=Blueprint('main',__name__)

@main.route("/")
def index():
    return render_template('homepage.html')
# DB Backup 
@main.route("/backup")
def backupdb():
    conn = sqlite3.connect(os.path.join('./app', 'diabetespred.sqlite3'),check_same_thread=False) 
    with io.open('backupdatabase_dump.sql', 'w') as p:   
        # iterdump() function
        for line in conn.iterdump(): 
            p.write('%s\n' % line)
    print(' Backup performed successfully!')
    print(' Data Saved as backupdatabase_dump.sql')
    return redirect(url_for('main.index'))
    conn.close()
# DB Restore
@main.route("/restore")
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
    return redirect(url_for('main.index'))
# MSG SEND
@main.route("/sendmsg")
def sendmsg():
    sendtestmsg()
    return redirect(url_for('main.index'))