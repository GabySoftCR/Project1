CREATE TABLE books2 (
    book_id SERIAL PRIMARY KEY,
    isbn  VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);
CREATE TABLE users (
    unum SERIAL PRIMARY KEY,
    user_id VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    name VARCHAR NOT NULL
);
CREATE TABLE reviews (
    rev_id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    userid VARCHAR NOT NULL,
    review VARCHAR NOT NULL
);
INSERT INTO books2 (isbn, title, author, year) VALUES
('200',	'Programming',	'Gabriela Pacheco',	2020);

SELECT * FROM books;

FROM 'books.csv' DELIMITER ',' CSV HEADER;

create unique index users_lemail_idx on users (lower(user_id));
