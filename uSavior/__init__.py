from flask import Flask
from flask_mail import Mail, Message

app = Flask("uSavior")
app.secret_key = 'save your grades'
app.config["MONGO_URI"] = "mongodb+srv://abdullah201:saveyourgrades@abdullah1065.hhjja0s.mongodb.net/uSavior"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'usavior.info@gmail.com'
app.config['MAIL_PASSWORD'] = 'knixkdijhtiqcqqr'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'usavior.info@gmail.com'
mail = Mail(app)

from uSavior.controllers import *


