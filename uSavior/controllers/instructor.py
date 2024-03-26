from flask import session, render_template, request, redirect
from flask_mail import Message
from datetime import date, datetime
from uSavior import app, mail

import bcrypt

from .home import *
from uSavior.models.instructor_model import *

@app.route("/instructor_login", methods = ['POST', 'GET'])
def instructor_login():
    if request.method == 'GET': 
        if 'ins_email' in session.keys(): return redirect('/instructor_dashboard')
        return render_template('instructor/instructor_login.html', **locals())
    elif request.method == 'POST':
        recieved = request.form
        found = db_instructor_details(recieved['email'])
        if found and bcrypt.checkpw(recieved['password'].encode('utf-8'), found['password']): 
            session['ins_email'] = recieved['email']
            return redirect('/instructor_dashboard')
        else: return redirect('/instructor_login') 


@app.route("/instructor_applyNow", methods = ['POST', 'GET'])
def instructor_registration():
    if request.method == 'GET': 
        if 'ins_email' in session.keys(): return redirect('/instructor_dashboard')
    elif request.method == 'POST':
        recieved = request.form
        found = db_instructor_details(recieved['email'])
        if found is not None: return redirect('/instructor_applyNow')
        file = request.files['upload']
        if file and file.filename.endswith('.pdf'):
            pdf_content = file.read()
        msg = Message('Thank You for Applying as an Instructor at uSavior', recipients=[recieved['email']])
        msg.body = f"Dear {recieved['lastname']}, \n\nWe, the uSavior team, are sincere gratitude for taking the time and effort to apply for the position of an instructor with us. We will carefully review your application. If selected, we would love to learn more about your teaching philosophy, innovative ideas, and your vision for enhancing the learning experience of our students.Once again, thank you for expressing interest in joining uSavior. We genuinely appreciate your interest in contributing to our community.\n\nBest regards,\nuSavior Team"
        mail.send(msg)
        db_instructor_register(dict(recieved),pdf_content)
        return redirect('/home')      
    return render_template('instructor/instructor_applyNow.html')


@app.route("/instructor_dashboard")
def instructor_dashboard():
    if 'ins_email' not in session.keys(): return redirect('/instructor_login')
    data = db_instructor_details(session['ins_email'])
    return render_template('instructor/instructor_dashboard.html', **locals())


@app.route("/instructor_edit_profile", methods = ['POST', 'GET'])
def instructor_edit_profile():
    if request.method == 'GET':
        if 'ins_email' not in session.keys(): return redirect('/instructor_login')
        data = db_instructor_details(session['ins_email'])
        return render_template('instructor/instructor_editProfile.html', **locals())
    elif request.method == 'POST':
        recieved = request.form
        db_instructor_editProfile(dict(recieved),session['ins_email'])
        return redirect('/instructor_dashboard')

@app.route("/instructor_my_courses")
def instructor_my_courses():
    if 'ins_email' not in session.keys(): return redirect('/instructor_login')
    return render_template('instructor/instructor_myCourses.html', **locals())

@app.route("/instructor_view_AllCourses")
def instructor_view_AllCourses():
    if 'ins_email' not in session.keys(): return redirect('/instructor_login')
    return render_template('instructor/instructor_ViewAllCourses.html', **locals())

@app.route("/instructor_upload_video")
def instructor_upload_video():
    if 'ins_email' not in session.keys(): return redirect('/instructor_login')
    return render_template('instructor/instructor_upload_video.html', **locals())

@app.route("/instructor_ChangePassword", methods = ['POST', 'GET'])
def instructor_ChangePassword():
    if request.method == 'GET':
        if 'ins_email' not in session.keys(): return redirect('/instructor_login')
        return render_template('instructor/instructor_ChangePassword.html', **locals())
    elif request.method == 'POST':
        recieved = request.form
        if recieved['password'] == recieved['r_password']:
            hashed_password = bcrypt.hashpw(recieved['password'].encode('utf-8'), bcrypt.gensalt())
            db_instructor_ChangePassword(session['ins_email'],hashed_password)
        return redirect('/instructor_dashboard')


#-----------------------------------------------------------------------------------
@app.route("/instructor_logout")
def instructor_logout():
    if 'ins_email' in session.keys():
        session.pop('ins_email')
    return redirect('/home')