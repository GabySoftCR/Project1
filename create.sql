CREATE TABLE books (
    isbn PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);
CREATE TABLE users (
    userid PRIMARY KEY,
    password VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
);
CREATE TABLE reviews (
    rev_id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    userid VARCHAR NOT NULL,
    review VARCHAR NOT NULL,
);
