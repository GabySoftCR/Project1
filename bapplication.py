import os
import psycopg2

from flask import Flask, session, render_template, request
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


@app.route("/")
def index():
    welcome=True
    return render_template("index.html", welcome=welcome)

@app.route("/out")
def out():
    welcome = False
    session.pop("username",None)
    return render_template("index.html", welcome=welcome)

@app.route("/start", methods=["POST"])
def start():
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    user_id = user_id.lower()
    session.pop("username",user_id)
    user=db.execute("SELECT user_id, password, name FROM users WHERE user_id = :user_id",
            {"user_id": user_id}).fetchone()
    #if password == user.password :
    return render_template("start.html", user_id=user_id, name=user.name, password=user.password)
    #else:
    #    return print ("Wrong password")


@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/adduser", methods=["POST"])
def adduser():
    user_id = request.form.get("user_id")
    password = request.form.get("pass1")
    name = request.form.get("name")
    user_id = user_id.lower()
    try:
        db.execute("INSERT INTO users (user_id, password, name) VALUES (:user_id, :password, :name)",
                    {"user_id": user_id , "password": password, "name": name})
        db.commit()
        return render_template("start.html", user_id=user_id, name=name)
    except :
        return "User ID exist"
