import os
import requests

from flask import Flask, session, render_template, request,flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

res = requests.get(url="https://www.goodreads.com/book/review_counts.json", params={"key": "l5jvvdnbvH2AUznwun7cw", "isbns": "9781632168146"})

@app.route("/",methods=["GET","POST"])
def logIn():
    if (request.method=="POST"):
        session.clear()
        user=request.form.get('user',None)
        password=request.form.get('password',None)
        if user is None or user == '':
            return render_template("error.html",message='user id cannot be blank')
        if password is None or user == '':
            return render_template("error.html",message='password cannot be blank')
    
        if db.execute("SELECT * FROM users WHERE userid = :user",{"user":user}).rowcount == 0:
            return render_template("error.html",message="""user id doesn't exist""")
    
        rows=db.execute("SELECT * FROM users WHERE userid= :user",{"user":user}).fetchone()

        if rows[2] == password:
            session["userid"]=rows[1]
            session["name"]=rows[3]
            return render_template("books.html",userid=session["userid"],name=session["name"])
        else:
            return render_template("error.html",message='user and password do not match')
    else:
        return render_template("index.html")

#Catches createAccountMain
@app.route("/createAccountMain",methods=["GET","POST"])
def createAccountMain():

    session.clear()
     #Get form names
    if request.method == "POST":
        name = request.form.get('name',None)
        user = request.form.get('user',None)
        password = request.form.get('password',None)

        if name is None or name == '':
            ################### DONT FORGET RETURN in render template #####################
            return render_template("error.html", message='name cannot be empty')

        if user is None or user == '':
            return render_template("error.html", message='user id cannot be empty')

        if password is None or password == '':
            return render_template("error.html", message='password cannot be empty')


        #Insert into DB 
        if db.execute("SELECT * FROM users WHERE userid = :user", {"user":user} ).rowcount == 0:
            db.execute("INSERT INTO users (userid,password,name) VALUES (:user,:password,:name)",{"user": user,"password": password,"name": name})
            ##############VERY IMPORTANT##################
        else:
            return render_template("error.html", message='User already existing id')
    
    db.commit()
    return render_template("createAccountMain.html")
    
@app.route("/search")
def search():
    searchVal=request.args.get('searchVal') #agrs for GET method
    if not request.args.get("searchVal"):
        return render_template("error.html",message='Search value cannot be empty')
    searchVal = searchVal.title() #this ignores Case sensitive and always use upperCase#
    searchVal = '%'+searchVal+'%'
    rows = db.execute("SELECT * FROM books WHERE name LIKE :searchVal OR ISBN LIKE :searchVal OR author LIKE :searchVal LIMIT 10",{"searchVal":searchVal})
    if(rows.rowcount==0):
        return render_template("error.html",message="No books found")
    books= rows.fetchall()
    db.commit()
    return render_template("error.html",message=books)
    