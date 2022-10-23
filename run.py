from app import app,db
import os
# importing the app variable in the __init__.py
if __name__ == "__main__":
    # for creating the db
    if not os.path.exists(os.path.join('./app', 'diabetespred.sqlite3')):
        db.create_all()
    app.run(debug=True)
    