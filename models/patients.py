
class Patients(db.Model):
    fname=db.Column("firstname",db.String(100))
    lname=db.Column("lastname",db.String(100))
    email=db.Column("email",db.String(100))
    password=db.Column("password",db.String(20))
    gender=db.Column("gender",db.String(20))
    dateofbirth=db.Column("DoB",db.String(20))
    contact=db.Column("contact",db.String(20))
    county=db.Column("county",db.String(20))
    area=db.Column("Region",db.String(20))
    uname=db.Column("username",db.String(20))
    def __init__(self,db,fname,lname,email,password,gender,dateofbirth,contact,county,area,uname):
        self.id=db.Column("id",db.Integer,primary_key=True)
        self.db=db
        self.fname=fname
        self.lname=lname
        self.email=email
        self.password=password
        self.gender=gender
        self.dateofbirth=dateofbirth
        self.contact=contact
        self.county=county
        self.area=area
        self.uname=uname
    if __name__=="main":
        db.create_all()
        app.run(debug=True)