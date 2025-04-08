CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE topics (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id), 
  topic_id INT NOT NULL REFERENCES topics(id),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_actions (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id), 
  action_type VARCHAR(20) NOT NULL, 
  action_time TIMESTAMP DEFAULT NOW(),
  status VARCHAR(10) NOT NULL, 
  target_id INT, 
  server_response TEXT
);