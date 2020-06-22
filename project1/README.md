# Project 1
Web Programming with Python and JavaScript

# Project1 - Books Review Website 
by Gabriela Pacheco P, email 
gabypacheco@me.com
Developed using Flask, python and psql.  Database hosted by HEROKU

Project Objectives, were definitely achieved.  When I started working felt stuck and as I worked started to fell fluent.  Learned a lot of python and SQL and Flask.  Part of my struggle was with syntax,  many errors occurred because I misplaced a coma or apostrophe or indentation. Had to read and research plenty to render a working website that I felt comfortable with.

#Getting Started.
Database tables created using psql db_url. 
Detail of tables and indexes in create.sql.

Database table books rows are importes using import.py that reads lines in books.csv and insert row in the books table.

#Configure enviroment.
export FLASK_APP=application.py;
export FLASK_DEBUG=1; (optional)
export DATABASE_URL=postgres://hifxvmlumisjnk:63bc0c393731651e4a5a2aad183ebf4035e9caa931010a42d4cf2e5828b896df@ec2-18-232-143-90.compute-1.amazonaws.com:5432/d4erbortof2k5p

Flask run

#Style and navigation
 Extended thru the website pages using layout.html.  
The navigation bar allows user navigation to search page, log out and goodreads api

#/ 
Starts by rendering  index.html for user login.  On this page registered users log in to use the application or can follow link to sign in.  Here session is cleared for safety.

#/signin
Renders signin.html were user must  provide: 
•	a user id that should match an email address although the app does not verify it to be a working email.  Email is  user_id is saved in the table using lower() function. Input type is email.
•	name: The user name
•	password: A string that should not contain escape or special characters.  The password string is verified to match against a second input field. Input type is password. 

On submit the form goes to the app route /adduser 
User can also go back to index.html to login following a link.

#/adduser
Here we get the information from signin.html and try to add user to users table in database.  If the user already exists an error is displayed and displays signin.html to try another user id.  The If user_id is unique then user information is inserted into users table and index.html is displayed so that user can register and start using the app.

#/login

Once the provides a valid user_id (email) and password, both required in index.html here we check that the user exist un users table and that password provided match password in users table.  User_id is compared using lower function as user_id is saved in lower case.  In case user does not exist or password does not match a message is displayed and index.html is displayed, else we open session registering  user_s  and user_id in the session variable and redirect to search_any.html.

#/search
Renders search_any.html – Used in the navigation menu.
Search_any.html, consist of a required text input, were the user can type the title, author or ISBN to search for a book.  User can provide a partial string. On submit we navigate to /books route .

#/books
Gets the string form search.html.  With the string we search books table by title, author or isbn using “like” so that if the string matches the content or part of the content of any column we can list the matching results.  Here we also use the lower function as there is case sensitivity and we don’t want to miss a match if the user type, for example, a authors name without capitals.  An index ind_any_low was created for this purpose.  In case the string searched has no match a message is emitted and the search_any.html displayed again.  In case we get match we go to the books.html.  On this template we list all matching rows as urls so that the user can choose the book to review.  On action we navigate /book/<book_id> the book_id in this case is the serial number book_s column in books table.
Here we do several things.
1.	We get sure that the books exist in the books database. If not a message is rendered and go back to search_any.html
2.	Search reviews table for any reviews submitted by website users to list on the book.html.  If no reviews available a message is also included.
3.	Get a json object from Goodreads api so that we can include from this site the average rating and number of ratings for this particular book, to display this data on the book.html.  If there is no data for this book a message is prepared
4.	Render book.html template with all the book information.

Book.html template, has two input fields, one so that user can provide a rating 1-5 of the book and another to include comments for the rating.  It also display book information:
•	Title, author, isbn and year published.   The isbn is given as a url link to /api/<isbn_id> and get a JSON constructed by the website.,  
•	Reviews submitted on this site:  Rating as start (1-5) and users comments. 
•	Goodreads average rating and numer of ratings for the book
•	Messages.
On action/submit button the user review is submitted to /addreview.

#/add_review
Gets book info to add submitted review to reviews table.  If areview for the book from the user already exist a message is given in other case the review is inserted in reviews table a succsess message is algo given.  To check for uniqness an index was created for the table using user_s  and book_s .
After adding review we render search_any. html template.

#/api
Renders template api.html so that user can input a requires text string named isbn_id corresponding to any ISBN number, on action the app is redirected to /api/<isbn_id> .   The app can access this route from the navigation bar or by clicking the isbn link in the book.html page.

#/greads
/api/<isbn_id>
api goodreads key=XxNpydjOyqyYduFrF5sqVA

A request to goodreads api method is made using the key, obtained from goodreads website, and the isbn to search.
If the status_code is 200 then with the received json and book info from database a new json is built and rendered.  We also check that the isbn has correspondence in books database, if not another message is provided and no json is constructed.  Tried to search if any goodreads method would provide the book info when missing but the only method found rendered an xml object. 
If the request si not successful an error 400 code is in order and we go back to the /api route.

Resulting json:

#/out
Route to properly log out from the website, session is finished and cleared.

Static folder contains images used in website

Questions? gabypacheco@me.com


