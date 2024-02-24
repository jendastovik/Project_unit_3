-- DROP TABLE IF EXISTS parties;
-- DROP TABLE IF EXISTS transactions;
-- DROP TABLE IF EXISTS employees;
-- DROP TABLE IF EXISTS discs;
-- DROP TABLE IF EXISTS orders;

CREATE TABLE IF NOT EXISTS parties (
  id INTEGER PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  points INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY,
  sender_id INTEGER REFERENCES parties(id),
  receiver_id INTEGER REFERENCES parties(id),
  amount INTEGER,
  signature TEXT,
  employee_id INTEGER REFERENCES employee(id)
);

CREATE TABLE IF NOT EXISTS employees (
  id INTEGER PRIMARY KEY,
  username TEXT,
  password TEXT,
  email TEXT
);

CREATE TABLE IF NOT EXISTS discs (
  id INTEGER PRIMARY KEY,
  type TEXT,
  mass REAL,
  diameter REAL
);

CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY,
  disc_id INTEGER REFERENCES discs(id),
  quantity INTEGER,
  price REAL,
  employee_id INTEGER REFERENCES employee(id),
  color TEXT,
  image TEXT,
  customer_id INTEGER REFERENCES parties(id)
);


