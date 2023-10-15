from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/sage_shastra'
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
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


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
    return render_template('contact.html')


@app.route("/post")
def post():
    return render_template('post.html')


app.run(debug=True)
