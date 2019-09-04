DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  UserID INTEGER PRIMARY KEY AUTOINCREMENT,
  Username TEXT UNIQUE NOT NULL,
  Password TEXT NOT NULL,
  Email TEXT NOT NULL
);

DROP TABLE IF EXISTS ToDoTable;

CREATE TABLE ToDoTable (
  ToDoID INTEGER PRIMARY KEY AUTOINCREMENT,
  Task TEXT NOT NULL,
  TaskDate TEXT NOT NULL,
  Username TEXT NOT NULL
);