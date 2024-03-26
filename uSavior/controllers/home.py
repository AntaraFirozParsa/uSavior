from flask import session, render_template, request, redirect, jsonify
from flask_mail import Message
from uSavior import app, mail

from uSavior.models.instructor_model import *
from uSavior.models.student_model import *

import random, string

@app.route("/home")
@app.route("/")
def home():
    return render_template('home/home.html')

@app.route("/forgotten_password/<type>", methods = ['POST', 'GET'])
def forgotten_password(type):
    if request.method == 'GET': 
        return render_template('home/forgotten_password.html', **locals())
    if request.method == 'POST':
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(12))
        recieved = request.form
        print(type)
        if type == 'student':
            db_student_ChangePassword(recieved['email'],password)
            msg = Message('Reset Your Password', recipients=[recieved['email']])
            msg.body = f"Dear Student, \n\nYou're receiving this email because you requested to reset your password. You can change your password again at any time from your Edir_Profile.\n\nYour new password: {password}\n\nBest regards,\nuSavior Team"
            mail.send(msg)
            
        elif type == 'instructor':
            db_instructor_ChangePassword(recieved['email'],password)
            msg = Message('Reset Your Password', recipients=[recieved['email']])
            msg.body = f"Dear Instructor, \n\nYou're receiving this email because you requested to reset your password. You can change your password again at any time from your Edir_Profile.\n\nYour new password: {password}\n\nBest regards,\nuSavior Team"
            mail.send(msg)
        return redirect('/home')
    

@app.route("/contacts")
def contacts():
    return render_template('home/contacts.html')

@app.route("/showError")
def showError():
    return render_template('home/showError.html', **locals())


