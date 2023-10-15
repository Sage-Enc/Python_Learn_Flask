from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


with open("config.json", "r") as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
if local_server:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']

db = SQLAlchemy(app)


class Contact(db.Model):
    # id,name,email,phno,msg,date
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phno = db.Column(db.String(10), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=True)


@app.route("/")
def home():
    return render_template('index.html', params=params)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/contact", methods={'GET', 'POST'})
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phno = request.form.get('phno')
        msg = request.form.get('msg')

        entry = Contact(name=name, email=email, phno=phno, msg=msg, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)


@app.route("/post")
def post():
    return render_template('post.html', params=params)


app.run(debug=True)
