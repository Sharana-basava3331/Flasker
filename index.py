from flask import Flask,render_template,request,flash
from flask_wtf import FlaskForm
from  wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
#old  database sqlalchemy
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///users.db'

# #new database mysql
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/users"
#adding  csrf
app.config["SECRET_KEY"]="this is secreate key"
#intalizing database
db=SQLAlchemy(app)

#creating model

class users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False,unique=True)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    #create  a string
    def __repr__(self):
        return '<name %r>' % self.name
    

a=datetime.utcnow

class name_form(FlaskForm):
    name=StringField("what is your name",validators=[DataRequired()])
    email=StringField("enter the email",validators=[DataRequired()])
    submit=SubmitField("submit")

#creating the home page 
@app.route("/")
def home():
    return render_template("home.html")

#creating the index page
@app.route("/index")
def index():
    name="john"
    return render_template("index.html",index_name=name)

@app.route("/user/<name>")
def user(name):
    
    return render_template("user.html",uname=name)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500

@app.route('/name',methods=["GET","POST"])
def name():
    name=None
    
    form=name_form()
    
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=""
        flash("form submitted succesfully!")
    return render_template("name.html",name=name,form=form)
    
@app.route("/user/new",methods=["GET","post"])
def new_user():
    name=None
    email=None
    form=name_form()
    
    if form.validate_on_submit():
        
        val_user=users.query.filter_by(email=form.email.data).first()
        if val_user is None:
            name=form.name.data
            email=form.email.data
            
            new_user=users(name=name,email=email)
            db.session.add(new_user)
            db.session.commit()
            flash("user added sucessfully")
        form.name.data=""
        form.email.data=""
        
    all_users=users.query.order_by(users.date)
    return render_template("new_user.html",form=form,all_users=all_users)



if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
