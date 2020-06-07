import os

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
    return render_template("index.html", welcome=welcome)

@app.route("/start", methods=["POST"])
def start():
    userid = request.form.get("userid")
    return render_template("start.html", userid=userid)

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/adduser", methods=["POST"])
def adduser():
    return "Aqui se agregua el usuario"
