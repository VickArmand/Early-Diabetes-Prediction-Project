BEGIN TRANSACTION;
CREATE TABLE admin_credentials (
	id INTEGER NOT NULL, 
	username VARCHAR(20) NOT NULL, 
	password VARCHAR(20) NOT NULL, 
	date_posted DATETIME NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	adminregistered INTEGER NOT NULL, 
	role VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	FOREIGN KEY(adminregistered) REFERENCES admins (id)
);
INSERT INTO "admin_credentials" VALUES(1,'MugechiVictor','$2b$12$WVuU4dgH3jq5OvVp./0r2un03P77LY0wihXvLMLYyWHMz3plk4s4O','2022-10-11 03:46:25.398571','Activated',1,'Super Admin');
INSERT INTO "admin_credentials" VALUES(2,'jencarson','$2b$12$2XGJ.FLIJEJbdS8W5FN6muPMLxW9EiH9Ra/xlqFRZkjxjtpETu9Ti','2022-10-11 03:50:56.133195','Activated',2,'General Admin');
CREATE TABLE admins (
	id INTEGER NOT NULL, 
	firstname VARCHAR(100) NOT NULL, 
	lastname VARCHAR(100) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	gender VARCHAR(20) NOT NULL, 
	"DoB" DATETIME NOT NULL, 
	contact VARCHAR(20) NOT NULL, 
	county VARCHAR(20) NOT NULL, 
	"Region" VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO "admins" VALUES(1,'Victor','Mugechi','victormaina1962@gmail.com','Male','2005-01-10 00:00:00.000000','+254727617870','Kiambu','Thika');
INSERT INTO "admins" VALUES(2,'Jennifer','Carson','jencarson@gmail.com','Male','2000-05-11 00:00:00.000000','+254793835669','Mombasa','Kwale');
CREATE TABLE doctor_credentials (
	id INTEGER NOT NULL, 
	username VARCHAR(20) NOT NULL, 
	password VARCHAR(20) NOT NULL, 
	specialty VARCHAR(20) NOT NULL, 
	date_posted DATETIME NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	doctorregistered INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	FOREIGN KEY(doctorregistered) REFERENCES doctors (id)
);
INSERT INTO "doctor_credentials" VALUES(1,'kencarson','$2b$12$TnBX15DcY2yRwe9k2TlD0uOHkfTNisl/pEmP5uqRoCjR9MoRwPMWK','Treatment','2022-10-11 19:05:08.161503','Activated',1);
CREATE TABLE doctors (
	id INTEGER NOT NULL, 
	firstname VARCHAR(100) NOT NULL, 
	lastname VARCHAR(100) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	gender VARCHAR(20) NOT NULL, 
	"DoB" DATETIME NOT NULL, 
	contact VARCHAR(20) NOT NULL, 
	county VARCHAR(20) NOT NULL, 
	"Region" VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO "doctors" VALUES(1,'Kennedy','Carson','kencarson@gmail.com','Male','2010-01-01 00:00:00.000000','+254793835669','Mombasa','Kilifi');
CREATE TABLE patient_credentials (
	id INTEGER NOT NULL, 
	username VARCHAR(20) NOT NULL, 
	password VARCHAR(20) NOT NULL, 
	date_posted DATETIME NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	patientregistered INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	FOREIGN KEY(patientregistered) REFERENCES patients (id)
);
INSERT INTO "patient_credentials" VALUES(1,'MugechiVictor','$2b$12$l/MFo11kJoRUHxABz7ixPONiwRXEiQh3O4Xg/KBcp8Hr1xM4KOQgi','2022-10-11 19:26:05.135959','Activated',1);
INSERT INTO "patient_credentials" VALUES(2,'shebibnoah','$2b$12$AP1MD9e0stZDyBhf/YyQJeSa5W8/X68tIN1JSkXufbx.jzRTRQmj2','2022-10-18 17:48:46.939114','Activated',2);
CREATE TABLE patient_messages (
	id INTEGER NOT NULL, 
	title VARCHAR(50) NOT NULL, 
	body VARCHAR(1000) NOT NULL, 
	date_posted DATETIME NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	recipient INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(recipient) REFERENCES patients (id)
);
CREATE TABLE patients (
	id INTEGER NOT NULL, 
	firstname VARCHAR(100) NOT NULL, 
	lastname VARCHAR(100) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	gender VARCHAR(20) NOT NULL, 
	"DoB" DATETIME NOT NULL, 
	contact VARCHAR(20) NOT NULL, 
	county VARCHAR(20) NOT NULL, 
	"Region" VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO "patients" VALUES(1,'Victor','Mugechi','victormaina1962@gmail.com','Male','2005-09-11 00:00:00.000000','+254727617870','Meru','Nchiru');
INSERT INTO "patients" VALUES(2,'Noah','Shebib','shebibnoah@gmail.com','Male','1998-02-18 00:00:00.000000','+254727617870','Mombasa','Kwale');
CREATE TABLE predictions (
	id INTEGER NOT NULL, 
	glucose FLOAT NOT NULL, 
	insulin FLOAT NOT NULL, 
	"BMI" FLOAT NOT NULL, 
	age INTEGER NOT NULL, 
	outcome INTEGER NOT NULL, 
	date_predicted DATETIME NOT NULL, 
	patientpred INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(patientpred) REFERENCES patients (id)
);
INSERT INTO "predictions" VALUES(1,100.0,500.0,100.0,17,X'0100000000000000','2022-10-14 17:11:54.080083',1);
INSERT INTO "predictions" VALUES(2,100.0,500.0,100.0,17,X'0100000000000000','2022-10-14 17:25:50.586312',1);
INSERT INTO "predictions" VALUES(3,100.0,500.0,100.0,17,X'0100000000000000','2022-10-14 17:26:11.369261',1);
INSERT INTO "predictions" VALUES(4,100.0,500.0,100.0,17,X'0100000000000000','2022-10-14 20:01:48.201543',1);
COMMIT;
