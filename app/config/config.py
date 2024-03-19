class Config:
    import os
    SECRET_KEY=os.environ.get('SECRET_KEY')
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('EMAIL_USER')
    MAIL_PASSWORD=os.environ.get('EMAIL_PASS')
    SQLALCHEMY_DATABASE_URI='sqlite:///diabetespred.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS= False