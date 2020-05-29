import os
import csv

from csv import reader
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


file = open('/Users/karanpatel/Desktop/CS50 Harvard DONT DELETE/project1books-karan/books.csv')

reader = csv.reader(file)
next(reader)
for isbn,title,author,year in reader:
    year=int(year,base=10)
    db.execute("INSERT INTO books (name,ISBN,author,year) VALUES (:title,:isbn,:author,:year)",{"title":title,"isbn":isbn,"author":author,"year":year})
    print(f"Added book {title} to database.")
db.commit()
print(f"ADDED ALL BOOKS TO DATABASE")


    


    