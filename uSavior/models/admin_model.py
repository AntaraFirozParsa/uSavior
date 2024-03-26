from .home_model import db, fs
from datetime import date, datetime
from bson.objectid import ObjectId

def db_admin_details(email):
    found = db.admin.find_one({'email':email})
    return found

def db_admin_verify(email, password):
    found = db.admin.find_one({'email':email,'password':password})
    return found

def db_admin_InsManagement():
    datas = db.instructor.find({'applyStatus': 'Pending'})
    return datas

def db_admin_StuManagement():
    datas = db.student.find()
    return datas

def db_admin_getCV(file_id):
    pdf = fs.get(ObjectId(file_id))
    return pdf

