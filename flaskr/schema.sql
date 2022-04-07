-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS like;
DROP TABLE IF EXISTS report;

PRAGMA foreign_keys = ON;

CREATE TABLE user (
  -- required fields
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  date_of_birth DATE NOT NULL,
  password TEXT NOT NULL,
--  last_tries TEXT, # TODO implement counter for failed login attempts
  accreditation TEXT NOT NULL DEFAULT user, -- 0 = banned, 1 = user, 2 = moderator, 3 = admin
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  -- optional fields for account info
  profile_pic TEXT,
  email TEXT,
  first_name TEXT,
  bio TEXT,

  class_number TEXT,
  class_level TEXT,
  speciality TEXT,

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

CREATE INDEX idx_user_username ON user (username); -- index for username for searching and user profile page

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  message TEXT NOT NULL,
  user_id INTEGER,
  status TEXT DEFAULT visible, -- visible, hidden
  anonymous BOOLEAN NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  edited BOOLEAN NOT NULL DEFAULT 0,
  edited_at TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  message TEXT NOT NULL,
  post_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  anonymous BOOLEAN NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
  FOREIGN KEY (post_id) REFERENCES post (id) ON DELETE CASCADE
);

CREATE TABLE like (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  post_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
--  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (post_id) REFERENCES post (id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE report (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  post_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,

  FOREIGN KEY (post_id) REFERENCES post (id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);