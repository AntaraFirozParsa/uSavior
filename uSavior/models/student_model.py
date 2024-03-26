from .home_model import db

def db_student_register(info):
    db.student.insert_one(dict(info))


def db_student_details(email):
    found = db.student.find_one({'email':email})
    return found

def db_student_editProfile(info,email):
    db.student.update_one({'email':email},{'$set':{'name':info['name'].upper(),'contact':info['contact'],'address':info['address']}})

def db_student_ChangePassword(email,password):
    db.student.update_one({'email':email},{'$set':{'password':password,'password_repeat':password}})