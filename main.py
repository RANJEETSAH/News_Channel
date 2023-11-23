from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

local_server=True

with open('config.json','r', encoding='utf-8') as c:
    params = json.load(c)["params"]



app = Flask(__name__)

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
    if request.method=='POST':
        pass
    else:
        return render_template("dashboard.html", params=params)
 
@app.route("/index")
def index1():
    return render_template("index.html", params=params)
@app.route("/about")
def about():
    return render_template("about.html", params=params)
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
app.run(debug=True, host = "192.168.237.224")