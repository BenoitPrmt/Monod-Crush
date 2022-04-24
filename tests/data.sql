INSERT INTO user (username,dateOfBirth, password, admin)
VALUES
  ('user','2004-07-01', 'pbkdf2:sha256:260000$j1yvJi5yhb2HmR6T$79a8aebea29853932285e324c925beec0b2b0637ebf00e048301b2f59c17670e', 0),
  ('admin', '2004-01-07', 'pbkdf2:sha256:260000$mKgiehuI9Pjl8LWD$70165e84779168d1cc6f96197c6ab044e0a7d1dfcfc1406b9a9e2c31c47735ae', 1);

INSERT INTO post (body, author_id, anonymous, created)
VALUES
  ('test body', 1,  1, "2018-01-01 22:54:14");
