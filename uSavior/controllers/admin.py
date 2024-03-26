from flask import session, render_template, request, redirect, send_file
from flask_mail import Message
from datetime import date, datetime
from uSavior import app, mail

from .home import *
from uSavior.models.admin_model import *
from uSavior.models.instructor_model import *

import random, string, bcrypt


@app.route("/admin", methods = ['POST', 'GET'])
@app.route("/admin_login", methods = ['POST', 'GET'])
def admin_login():
    if request.method == 'GET': 
        if 'admin_email' in session.keys(): return redirect('/admin_dashboard')
        return render_template('admin/admin_login.html', **locals())
    elif request.method == 'POST':
        recieved = request.form
        found = db_admin_verify(recieved['email'],recieved['password'])
        if found is None: return redirect('/admin_login') 
        session['admin_email'] = recieved['email']
        return redirect('/admin_dashboard')

@app.route("/admin_dashboard")
def admin_dashboard():
    if 'admin_email' not in session.keys(): return redirect('/admin_login')
    data = db_admin_details(session['admin_email'])
    return render_template('admin/admin_dashboard.html', **locals())

@app.route("/admin_StuManagement")
def admin_StuManagement():
    if 'admin_email' not in session.keys(): return redirect('/admin_login')
    all_info = db_admin_StuManagement()
    return render_template('admin/admin_StuManagement.html', **locals())

@app.route("/admin_InsManagement")
def admin_InsManagement():
    if 'admin_email' not in session.keys(): return redirect('/admin_login')
    all_info = db_admin_InsManagement()
    return render_template('admin/admin_InsManagement.html', **locals())
    
@app.route('/download_cv/<file_id>')
def download_CV(file_id):
    pdf = db_admin_getCV(file_id)
    rename = db_instructor_getName((file_id))
    response = send_file(pdf, as_attachment=True, download_name=f'{rename}_CV.pdf', mimetype='application/pdf')
    return response

@app.route("/admin_approve_Ins/<file_id>")
def admin_approve_Ins(file_id):
    if 'admin_email' not in session.keys(): return redirect('/admin_login')
    name, email = db_instructor_getInfo(file_id)
    msg = Message('Congratulations on Your Selection as an Instructor at uSavior!', recipients=[email])
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db_instructor_approve(file_id, hashed_password)
    msg.body = f"Dear {name}, \n\nWe, the uSavior team, are thrilled to inform you that you have been selected as an Instructor.\n\nYour application and interview impressed our team, and we were thoroughly impressed with your qualifications, experience, and genuine passion for education. We believe that your expertise and dedication will make a significant positive impact on our students and contribute to the growth of uSavior.Once again, congratulations on becoming a part of uSavior. We eagerly look forward to your valuable contributions and a successful journey together.\n\nLogin mail: {email}\nLogin password: {password}\nYou can change your password again at any time from your Edir_Profile.\n\nBest regards,\nuSavior Team"
    mail.send(msg)
    return redirect('/admin_InsManagement')

@app.route("/admin_delete_Ins/<file_id>")
def admin_delete_Ins(file_id):
    if 'admin_email' not in session.keys(): return redirect('/admin_login')
    name, email = db_instructor_getInfo(file_id)
    db_instructor_delete(file_id)
    msg = Message('Update on Your Application for the Instructor Position at uSavior', recipients=[email])
    msg.body = f"Dear {name}, \n\nHope this email finds you well.  We truly value the time and effort you invested in your application and the opportunity to learn more about your qualifications and passion for education. After carefully reviewing all applications and considering various factors, we have made our final selection for the Instructor position. While your application impressed us, we regret to inform you that we have chosen another candidate whose qualifications more closely match the specific needs and requirements of the role at this time.\n\nPlease know that this decision does not diminish the value of your skills and experiences. We had a competitive pool of applicants, and the selection process was challenging due to the high caliber of individuals who expressed interest in joining our team.We wish you all the best in your professional endeavors.\n\nBest regards,\nuSavior Team"
    mail.send(msg)
    return redirect('/admin_InsManagement')

#-----------------------------------------------------------------------------------
@app.route("/admin_logout")
def admin_logout():
    if 'admin_email' in session.keys():
        session.pop('admin_email')
    return redirect('/home')