from uSavior import app
from flask_pymongo import PyMongo, GridFS
db = PyMongo(app).db
fs = GridFS(db)
