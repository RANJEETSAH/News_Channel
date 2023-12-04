from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import os

local_server=True

with open('config.json','r', encoding='utf-8') as c:
    params = json.load(c)["params"]



app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config['UPLOAD_FOLDER'] = params['upload_location']

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bharat'
db = SQLAlchemy(app)
class Contacts(db.Model):
    S_No = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Phone_Number = db.Column(db.String(120), unique=True, nullable=False)
    Message = db.Column(db.String)
    Date = db.Column(db.String(80), nullable=True)
    Email = db.Column(db.String(120), nullable=False)

class Posts(db.Model):
    S_No = db.Column(db.Integer, primary_key=True)
    Author = db.Column(db.String(50), nullable=False)
    Title = db.Column(db.String(80), nullable=False)
    Slug = db.Column(db.String(120), unique=True, nullable=False)
    Content = db.Column(db.String)
    Date = db.Column(db.String(80), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)

@app.route("/")
def index():
    posts=Posts.query.filter_by().all() [0:params['no_of_posts']]
    return render_template("index.html", params=params, posts=posts)
@app.route("/login", methods=['GET', 'POST'])
def login():
    posts=Posts.query.filter_by().all()
    if ('user' in session and session['user'] == params['admin_user']):
        return render_template('dashboard.html', params=params,posts=posts )

    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['admin_user'] and userpass == params['admin_password']):
            session['user']  = username
            return render_template('dashboard.html', params=params, posts=posts)

    return render_template("login.html", params=params)
 
@app.route("/index")
def index1():
    return render_template("index.html", params=params)
@app.route("/about")
def about():
    return render_template("about.html", params=params)

@app.route("/edit/<string:S_No>", methods = ['GET','POST'])
def edit(S_No):
    if ('user' in session and session['user'] == params['admin_user']):
        if request.method == 'POST':
            author = request.form.get('author')
            title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()

            if S_No == "0":
                post = Posts(Author=author, Title=title, Slug=slug, Content=content, img_file=img_file, Date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post=Posts.query.filter_by(S_No=S_No).first()
                post.Author=author
                post.Title=title
                post.Slug=slug
                post.Content=content
                post.img_file=img_file
                post.Date=date
                db.session.commit()
                return redirect("/edit/"+S_No)
        post=Posts.query.filter_by(S_No=S_No).first()
        return render_template ('edit.html', params=params, S_No=S_No, post=post)

@app.route("/contact", methods = ['GET','POST'])
def contact():
        
    if (request.method=='POST'):
        """Add Entry to the Database"""
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        entry=Contacts(Name=name,Phone_Number=phone, Message=message, Date=datetime.now(), Email=email)
        db.session.add(entry)
        db.session.commit()
    return render_template("contact.html", params=params)
@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post=Posts.query.filter_by(Slug=post_slug).first()
    return render_template("post.html", params=params,post=post)

@app.route("/uploader", methods = ['GET','POST'])
def uploader():
    if ('user' in session and session['user'] == params['admin_user']):
        if (request.method == 'POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded Successfully"


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/login')

@app.route("/delete/<string:S_No>", methods = ['GET','POST'])
def delete(S_No):
    if ('user' in session and session['user'] == params['admin_user']):
        post=Posts.query.filter_by(S_No=S_No).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/login')
        


app.run(debug=True, host = "192.168.234.224")