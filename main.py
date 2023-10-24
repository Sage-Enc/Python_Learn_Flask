from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json


with open("config.json", "r") as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['mail_user'],
    MAIL_PASSWORD=params['mail_pass'],
)

mail = Mail(app)

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


class Posts(db.Model):
    # id, title, img_name, slug, content, date
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    tagline = db.Column(db.String(256), nullable=False)
    img_name = db.Column(db.String(50), nullable=True)
    slug = db.Column(db.String(256), nullable=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.String(20), nullable=True)


@app.route("/edit/<string:id>", methods=["GET", "POST"])
def edit(id):
    if 'uname' in session and session['uname'] == params['admin_name']:
        if request.method == "POST":
            box_title = request.form.get('title')
            box_tagline = request.form.get('tagline')
            box_slug = request.form.get('slug')
            box_content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if id == '0':
                post = Posts(title=box_title, tagline=box_tagline, slug=box_slug, content=box_content, img_name=box_img, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(id=id).first()
                post.title = box_title
                post.tagline = box_tagline
                post.slug = box_slug
                post.content = box_content
                post.img_name = img_file
                db.session.commit()
                return redirect('/edit/'+id)
        post = Posts.query.filter_by(id=id).first()
        return render_template('edit.html', params=params, post=post)
    else:
        return render_template('signin.html', params=params)


@app.route("/dashboard", methods=["GET", "POST"])
def signin():
    if 'uname' in session and session['uname'] == params['admin_name']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)

    if request.method == "POST":
        username = request.form.get('uname')
        password = request.form.get('upword')
        if username == params['admin_name'] and password == params['admin_pword']:
            session['uname'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)
    return render_template('signin.html', params=params)


@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:5]
    return render_template('index.html', params=params, posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phno = request.form.get('phno')
        msg = request.form.get('msg')
        entry = Contact(name=name, email=email, phno=phno, msg=msg, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            subject=f"You Have Received A New Message from {name}",
            sender=email,
            recipients=[params['mail_user']],
            body=msg + "\n" + phno
        )
    return render_template('contact.html', params=params)


@app.route("/post/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)


app.run(debug=True)
