import os
import requests

from flask import Flask, session, render_template, request, jsonify, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = '650612CostaRica'

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
    session.pop("user_id", None)
    return render_template("index.html")

@app.route("/out")
def out():
    session.pop("user_id",None)
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    user_id = user_id.lower()

    try:
        user = db.execute("SELECT user_s, user_id, password, name FROM users WHERE user_id = :user_id",
            {"user_id": user_id}).fetchone()
        if password != user.password:
            flash("Invalid User/Password")
            return render_template("index.html")
        else:
            session['user_id'] = user_id
            session['user_s'] = user.user_s
            return render_template("search_any.html")
    except Exception as error:
        flash("Invalid User/Password")
        return render_template("index.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/adduser", methods=["POST"])
def adduser():
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if password != password2:
        flash("Verify Password - Not Matching")
        return render_template("signin.html")
    user_id = request.form.get("user_id")
    name = request.form.get("name")
    user_id = user_id.lower()
    try:
        db.execute("INSERT INTO users (user_id, password, name) VALUES (:user_id, :password, :name)",
                    {"user_id": user_id , "password": password, "name": name})
        db.commit()
        flash ("User registered.  Please log in.")
        return render_template("index.html")
    except Exception as error:
        flash("Try another user!")
        return render_template("signin.html")

@app.route("/search")
def search():
    if 'user_id' in session:
        return render_template("search_any.html")
    else:
        return redirect(url_for('out'))

@app.route("/books", methods=["POST"])
def books():
    s_str = request.form.get('s_str')
    s_str = s_str.lower()
    filter = "SELECT * FROM books WHERE lower(title) LIKE :s_str OR lower(author) LIKE :s_str OR lower(isbn) LIKE :s_str ORDER BY title ASC"
    """Old Search
    s_by = request.form.get('s_by')
    s_str = request.form.get('s_str')
    s_str = s_str.lower()
    filter = "SELECT * FROM books WHERE lower(" + s_by + ") LIKE :s_str ORDER BY " + s_by + " ASC"""""
    books = db.execute(filter,{"s_str": "%" + s_str + "%"}).fetchall()
    if not books:
        message = "No book matches search " + s_str
        flash(message)
        return render_template("search_any.html")
    return render_template("books.html", books=books)

@app.route("/books/<int:book_id>")
def book(book_id):
        """Lists info about a single book."""

        book = db.execute("SELECT * FROM books WHERE book_id = :book_id", {"book_id": book_id}).fetchone()

        if not book:
            flash("Book is not available in database")
            return render_template("search_any.html")
        else:
            session['book_id'] = book_id

            """Get all reviews"""
            reviews = db.execute("SELECT rating, review FROM reviews WHERE book_id = :book_id",
                                 {"book_id": book_id}).fetchall()
            if not reviews:
                flash("Be the first one to review this book on this site")

            """Get Goodreads data"""
            isbn_params = {"key": " XxNpydjOyqyYduFrF5sqVA", "isbns": book.isbn}
            res = requests.get('https://www.goodreads.com/book/review_counts.json', params=isbn_params)
            if res.status_code != 200:
                flash("Code 400: No data in for this book in Goodreads.")
            data = res.json()
            average = data['books'][0]['average_rating']
            count = data['books'][0]['ratings_count']
            return render_template("book.html", book=book, reviews=reviews, count=count, average=average)


@app.route("/add_review", methods=["POST"])
def add_review():
    book_id = session['book_id']
    rating = request.form.get('add_rating')
    review = request.form.get('add_review')
    user_s = session['user_s']
    try:
        db.execute("INSERT INTO reviews (book_id, user_id, rating, review) VALUES (:book_id, :user_s, :rating, :review)",
                    {"book_id": book_id , "user_s": user_s, "rating": rating, "review": review})
        db.commit()
        flash("Review succesfully added for this book.")
        return render_template("search_any.html", book=book)

    except Exception as error:
        flash("Book already reviewed by User. One comment per book.")
        return render_template("search_any.html", book=book)

@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "POST":
        isbn_id = request.form.get('isbn_id')
        return redirect(url_for('gread', isbn_id=isbn_id))
    else:
        return render_template("api.html")

@app.route("/api/<string:isbn_id>")
def gread(isbn_id):

    isbn_params = {"key": " XxNpydjOyqyYduFrF5sqVA", "isbns": isbn_id}
    res = requests.get('https://www.goodreads.com/book/review_counts.json', params=isbn_params)
    if res.status_code != 200:
        flash("ERROR 400: API request unsuccessful.")
        return render_template("api.html", err_isb=isbn_id)
        #return jsonify({"ERROR 400: API request unsuccessful."})
    else:
        data = res.json()
        average = data['books'][0]['average_rating']
        count = data['books'][0]['reviews_count']
        book = db.execute("SELECT * FROM books WHERE isbn = :isbn_id", {"isbn_id": isbn_id}).fetchone()
        if not book:
            message = "ERROR 404: ISBN " + isbn_id + " not in this Database"
            flash(message, "danger")
            return render_template("api.html")
        else:
            return jsonify({"title": book.title, "author": book.author, "year": book.year,
                       "isbn": isbn_id, "review_count": data["books"][0]["reviews_count"], "average_rating": data["books"][0]["average_rating"]})
        return render_template("isbn.html", **locals())
        #return render_template("isbn.html", data=data, book=book, count=count, average=average, my_json=my_json)

