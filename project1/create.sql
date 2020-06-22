CREATE TABLE books(
    book_id SERIAL PRIMARY KEY,
    isbn  VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);
CREATE TABLE users (
    user_s SERIAL PRIMARY KEY,
    user_id VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    name VARCHAR NOT NULL
);
CREATE TABLE reviews (
    rev_id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    review VARCHAR NOT NULL,
    rating INTEGER NOT NULL
);
ALTER TABLE users
  RENAME  unum TO user_s;


FROM 'books.csv' DELIMITER ',' CSV HEADER;

CREATE UNIQUE INDEX idx_user_book ON reviews (book_id, user_id);
CREATE INDEX idx_all_lower ON books (lower(title), lower(author), lower(isbn));
CREATE UNIQUE index users_lemail_idx on users (lower(user_id));

DELETE FROM reviews WHERE book_id = '10715';
DELETE FROM users WHERE user_id = 'lucycast@hotmail';


 books=db.execute("SELECT isbn, title, author, year FROM books WHERE :sb LIKE '%ss%",
            {"sb": sb}, {"ss": ss}).fetchall

 books=db.execute("SELECT isbn, title, author, year FROM books WHERE author LIKE '%way%",
            {"sb": sb}, {"ss": ss}).fetchall