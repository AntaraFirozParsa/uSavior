from .home_model import db, fs
from datetime import date, datetime
from bson.objectid import ObjectId

def db_instructor_register(info,pdf_content):
    pdf_id = fs.put(pdf_content, filename=f"{info['firstname']}.pdf")
    info['applyStatus'], info['cv'], info['password'], info['applyDate']= 'Pending', pdf_id, None, str(date.today())
    db.instructor.insert_one(dict(info))

def db_instructor_details(email):
    found = db.instructor.find_one({'email':email})
    return found

def db_instructor_getName(file_id):
    data = db.instructor.find_one({'cv': ObjectId(file_id)})
    name = data['firstname']+'_'+data['lastname']
    return name

def db_instructor_getInfo(file_id):
    data = db.instructor.find_one({'cv': ObjectId(file_id)})
    name = data['firstname']+' '+data['lastname']
    email = data['email']
    return name, email

def db_instructor_approve(file_id, password):
    data = db.instructor.find_one({'cv': ObjectId(file_id)})
    db.instructor.update_one({'email':data['email']},{'$set':{'applyStatus':'Approved', 'password': password}})

def db_instructor_delete(file_id):
    fs.delete(ObjectId(file_id))
    data = db.instructor.delete_one({'cv': ObjectId(file_id)})

def db_instructor_editProfile(info,email):
    firstname, lastname = info['name'].split()[0],info['name'].split()[1]
    db.instructor.update_one({'email':email},{'$set':{'firstname':firstname,'lastname':lastname,'contact':info['contact'],'address':info['address']}})
    
def db_instructor_ChangePassword(email,password):
    db.instructor.update_one({'email':email},{'$set':{'password':password}})