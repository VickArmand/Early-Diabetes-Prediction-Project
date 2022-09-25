from app import app
# importing the app variable in the __init__.py
if __name__ == "__main__":
    # for creating the db
    # db.create_all()
    app.run(debug=True)
    