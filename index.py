from flask import Flask,render_template,request,flash,redirect,url_for
from flask_wtf import FlaskForm
from  wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,EqualTo
from wtforms.widgets import TextArea
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime,date
from werkzeug.security import generate_password_hash,check_password_hash


app=Flask(__name__)
#old  database sqlalchemy
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///users.db'

# #new database mysql
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3306/users"
#adding  csrf
app.config["SECRET_KEY"]="this is secreate key"
#intalizing database
db=SQLAlchemy(app)
migrate=Migrate(app,db)# created the manage.py in same folder
# Initialize migration folder (only first time)
# flask db init
# # Generate a migration for model changes
# flask db migrate -m "Add age column to users"
# # Apply migration to the database
# flask db upgrade

#creating model
class users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False,unique=True)
    date=db.Column(db.DateTime,default=datetime.utcnow)
    # this is migrated
    color=db.Column(db.String(100))
    password_hash=db.Column(db.String(120),nullable=False)

    @property
    def password(self):
        raise AttributeError("password is not  accesable ")

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    #create  a string
    def __repr__(self):
        return '<name %r>' % self.name
    

a=datetime.utcnow

class name_form(FlaskForm):
    name=StringField("what is your name",validators=[DataRequired()])
    email=StringField("enter the email",validators=[DataRequired()])
    color=StringField("enter the color")
    submit=SubmitField("submit")
    cancel=SubmitField("Cancel")
    delete=SubmitField("Delete")
    password_hash=PasswordField("Password",validators=[DataRequired(),EqualTo("password_hash2",message="password must match")])
    password_hash2=PasswordField("Confirm Password")

# creating the login form
class Login(FlaskForm):
    email=StringField("Email",validators=[DataRequired()])
    password=PasswordField("Password")
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
# error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500

# name creation
@app.route('/name',methods=["GET","post"])
def name():
    name=None
    
    form=name_form()
    
    if form.validate_on_submit():
        name=form.name.data
        
        form.name.data=""
        flash(f"Form submitted successfully! Hello {name}")  # ✅ Flash message
        return redirect(url_for('name'))
        
    return render_template("name.html",name=name,form=form)

 #login page
@app.route("/login/",methods=["GET","POST"]) 
def login():
    email=None
    password=None
    form=Login()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        form.password.data=""
        form.email.data=""
        validate=users.query.filter_by(email=email).first()
        if validate:
            check_pwd=check_password_hash(validate.password_hash,password)
            return render_template("login.html",validate=validate,form=form,email=email,password=password,check_pwd=check_pwd)
        # return redirect(url_for('login'))

            flash("the user addesd")
    return render_template("login.html",form=form)

@app.route("/user/new",methods=["GET","post"])
def new_user():
    name=None
    email=None
    password=None
    form=name_form()
    if form.validate_on_submit():
        
        val_user=users.query.filter_by(email=form.email.data).first()
        if val_user is None:
            name=form.name.data
            email=form.email.data
            color=form.color.data
            password=generate_password_hash(form.password_hash.data,'pbkdf2:sha256')
            
            new_user=users(name=name,email=email,color=color,password_hash=password)
            db.session.add(new_user)
            db.session.commit()
            flash("user added sucessfully")
        form.name.data=""
        form.email.data=""
        form.password_hash.data=""
    all_users=users.query.order_by(users.date)
    
    
    return render_template("new_user.html",form=form,all_users=all_users)


#upadting to database
@app.route("/update/<int:id>",methods=["GET","POST"])
def update_id(id):
    form=name_form()
    name_update=users.query.get_or_404(id)
    if request.method=='POST' and form.submit.data:
        
        val_user=users.query.filter_by(email=form.email.data).first()
        if val_user is None:
            name_update.name=request.form['name']
            name_update.email=request.form['email']
            name_update.color=request.form['color']
            

            try:
                db.session.commit()
                flash("user updated succesfully ")
                return render_template("update.html",form=form,name_update=name_update)
            except:
                flash("user updated  unsuccesfull there is a problem...\n try again... ")
                return render_template("update.html",form=form,name_update=name_update)
        else:
            flash("user alredy exist")
            return render_template("update.html",form=form,name_update=name_update)
    elif form.delete.data:
        db.session.delete(name_update)
        db.session.commit()
        flash(f"the user {request.form['name']} deleted")
        return redirect(url_for("new_user"))
        
    elif form.cancel.data:
        return redirect(url_for("new_user"))
    else:
        return render_template("update.html",form=form,name_update=name_update,id=id)
    
@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete(id):
    form=name_form()
    value=users.query.get_or_404(id)
    try:
        db.session.delete(value)
        db.session.commit()
        flash("deleted succefully")
    except:
        flash("delete was unsuccefull")
    return redirect(url_for('new_user'))
    
# json file reading
@app.route("/date/")
def date_():
    f={
        "name":"demo",
        "age":12,
        "sal":23822
    }
    return f

# create posts db model
class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(120),nullable=False)
    author=db.Column(db.String(120),nullable=False)
    slug=db.Column(db.String(120),nullable=False)
    text=db.Column(db.String(120),nullable=False)
    date_time=db.Column(db.DateTime,default=datetime.utcnow)
    
# create posts form
class Post_form(FlaskForm):
    title=StringField("Title",validators=[DataRequired()])
    author=StringField("Authoor",validators=[DataRequired()])
    slug=StringField("slug",validators=[DataRequired()])
    text=StringField("Content",validators=[DataRequired()], widget=TextArea())
    submit=SubmitField("submit")
    view=SubmitField("View")

@app.route("/add-blog",methods=["GET","POST"])
def add_blog():
    
    form=Post_form()
    if form.validate_on_submit():
        post=Posts(title=form.title.data,author=form.author.data,slug=form.slug.data,text=form.text.data)
        
        form.title.data=""
        form.author.data=""
        form.text.data=""
        form.slug.data=""
        db.session.add(post)
        db.session.commit()
        flash("the blog added succefully")
    return render_template("add_blog.html",form=form)

@app.route("/view_blog/",methods=["GET","POST"])
def view_blog():
    view_posts=Posts.query.order_by(Posts.date_time)
    if view_posts:
        return render_template("view_blogs.html",view_posts=view_posts)

# indivusal post view
@app.route("/view_blog/<int:id>")
def update_blog(id):
    post=Posts.query.get_or_404(id)
    return render_template("post.html",post=post,id=id)

# editing the post
@app.route("/view_blog/update/<int:id>",methods=["GET","POST"])
def update_post(id):
    form=Post_form()
    post=Posts.query.get_or_404(id)
    if form.validate_on_submit():

        post.title=form.title.data
        post.author=form.author.data
        post.slug=form.slug.data
        post.text=form.text.data
        db.session.add(post)
        db.session.commit()
        flash("update  succefully")
        return redirect(url_for("update_blog",id=post.id))
    form.title.data=post.title
    form.author.data=post.author
    form.slug.data=post.slug
    form.text.data=post.text
    flash("viewing the valeus")
    return render_template("update_post.html",post=post,form=form)

#deleting the post
@app.route("/view_blog/delete/<int:id>",methods=["GET","POST"]) 
def delete_post(id):
    val=Posts.query.get_or_404(id)
    if val:
        db.session.delete(val)
        db.session.commit()
        
        
        flash("post got deleted..")
        return redirect(url_for("view_blog"))
        


    


    
   
        
   


if __name__=="__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
