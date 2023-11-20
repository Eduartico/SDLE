CREATE TABLE data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  key TEXT NOT NULL,
  value TEXT NOT NULL
);


INSERT INTO data (key, value) VALUES ('name', 'John');
INSERT INTO data (key, value) VALUES ('age', '42');
INSERT INTO data (key, value) VALUES ('city', 'London');
INSERT INTO data (key, value) VALUES ('country', 'UK');