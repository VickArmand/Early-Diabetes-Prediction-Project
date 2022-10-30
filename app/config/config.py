import os
class Config:
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('EMAIL_USER')
    MAIL_PASSWORD=os.environ.get('EMAIL_PASS')

    SQLALCHEMY_DATABASE_URI='sqlite:///diabetespred.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS= False