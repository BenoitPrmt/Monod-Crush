-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  -- required fields
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  admin INTEGER NOT NULL DEFAULT 0,

  -- optional fields for account info
  profilePic TEXT,
  email TEXT,
  firstName TEXT,
  description TEXT,
  dateOfBirth TIMESTAMP,

  class TEXT,
  speciality TEXT,
  bio TEXT,

  -- optional fields for social media
  -- store only the username/id not the full url
  facebook TEXT,
  twitter TEXT,
  instagram TEXT,
  linkedin TEXT,
  youtube TEXT,
  github TEXT,

  website TEXT
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  body TEXT NOT NULL,
  author_id INTEGER,
  anonymous INTEGER NOT NULL DEFAULT 1,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  text TEXT NOT NULL,
  post_id INTEGER NOT NULL,
  author_id INTEGER NOT NULL,
  anonymous INTEGER NOT NULL DEFAULT 1,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (author_id) REFERENCES user (id)
  FOREIGN KEY (post_id) REFERENCES post (id)
);