from flask import session, render_template, request, redirect
from flask_mail import Message
from datetime import date, datetime
from uSavior import app, mail
import bcrypt
from .home import *
from uSavior.models.student_model import *


@app.route("/student_login", methods = ['POST', 'GET'])
def student_login():
    if request.method == 'GET': 
        if 'stu_email' in session.keys(): return redirect('/student_dashboard')
        return render_template('student/student_login.html', **locals())
    elif request.method == 'POST':
        recieved = request.form
        found = db_student_details(recieved['email'])
        if found and bcrypt.checkpw(recieved['password'].encode('utf-8'), found['password']): 
            session['stu_email'] = recieved['email']
            return redirect('/student_dashboard')
        else: return redirect('/student_login')

        

@app.route("/student_registration", methods = ['POST', 'GET'])
def student_registration():
    message = None
    if request.method == 'GET': 
        if 'stu_email' in session.keys(): return redirect('/student_dashboard')
        return render_template('student/student_registration.html', **locals())
    elif request.method == 'POST':
        recieved = request.form.to_dict()
        found = db_student_details(recieved['email'])
        if found is not None: return redirect('/student_registration')
        elif recieved ['password'] != recieved ['password_repeat']: return redirect('/student_registration')
        hashed_password = bcrypt.hashpw(recieved ['password'].encode('utf-8'), bcrypt.gensalt())
        recieved ['password'], recieved ['password_repeat']= hashed_password, hashed_password
        db_student_register(dict(recieved))
        msg = Message('Welcome to uSavior! Confirmation of Your Join as a Student', recipients=[recieved['email']])
        msg.body = f"Dear {recieved['name']}, \n\nWe, the uSavior team, are delighted to inform you that your registration as a student has been accepted. Congratulations and a warm welcome to our educational community! Thanks for your acceptance to uSavior! We are thrilled to have you join our community of ambitious and talented students. We look forward to helping you embark on an enriching educational journey and making the most of your time at uSavior.\n\nBest regards,\nuSavior Team"
        mail.send(msg)
        return redirect('/student_login')      
    

@app.route("/student_dashboard")
def student_dashboard():
    if 'stu_email' not in session.keys(): return redirect('/student_login')
    data, today = db_student_details(session['stu_email']), date.today()
    date_of_birth = datetime.strptime(data['birthday'], "%Y-%m-%d").date()
    age = today.year - date_of_birth.year
    if today.month < date_of_birth.month or (today.month == date_of_birth.month and today.day < date_of_birth.day): age -= 1
    return render_template('student/student_dashboard.html', **locals())
   
    
@app.route("/student_edit_profile", methods = ['POST', 'GET'])
def student_edit_profile():
    if request.method == 'GET':
        if 'stu_email' not in session.keys(): return redirect('/student_login')
        data = db_student_details(session['stu_email'])
        return render_template('student/student_editProfile.html', **locals())
    elif request.method == 'POST':
        recieved = request.form
        db_student_editProfile(dict(recieved),session['stu_email'])
        return redirect('/student_dashboard')

@app.route("/student_my_courses")
def student_my_courses():
    if 'stu_email' not in session.keys(): return redirect('/student_login')
    return render_template('student/student_myCourses.html', **locals())

@app.route("/student_View_AllCourses")
def student_View_AllCourses():
    if 'stu_email' not in session.keys(): return redirect('/student_login')
    return render_template('student/student_ViewAllCourses.html', **locals())

@app.route("/student_View_Cart")
def student_View_Cart():
    if 'stu_email' not in session.keys(): return redirect('/student_login')
    return render_template('student/student_ViewCart.html', **locals())


@app.route("/student_play_video")
def student_play_video():
    if 'stu_email' not in session.keys(): return redirect('/student_login')
    return render_template('student/student_play_video.html', **locals())

@app.route("/student_video_list")
def student_video_list():
    if 'stu_email' not in session.keys(): return redirect('/student_login')
    return render_template('student/student_video_list.html', **locals())

@app.route("/student_ChangePassword", methods = ['POST', 'GET'])
def student_ChangePassword():
    if request.method == 'GET':
        if 'stu_email' not in session.keys(): return redirect('/student_login')
        return render_template('student/student_ChangePassword.html', **locals())
    elif request.method == 'POST':
        recieved = request.form
        if recieved['password'] == recieved['r_password']:
            hashed_password = bcrypt.hashpw(recieved['password'].encode('utf-8'), bcrypt.gensalt())
            db_student_ChangePassword(session['stu_email'],hashed_password)
        return redirect('/student_dashboard')
    
@app.route("/student_specific_course_details")
def student_specific_course_details():
    if 'stu_email' not in session.keys(): return redirect('/student_login')
    return render_template('student/student_specific_course_details.html', **locals())

#-----------------------------------------------------------------------------------
@app.route("/student_logout")
def student_logout():
    if 'stu_email' in session.keys():
        session.pop('stu_email')
    return redirect('/home')
