-- schema.sql

-- Turn off foreign key constraints temporarily
PRAGMA foreign_keys=off;

-- Start a new transaction
BEGIN TRANSACTION;

-- Create the 'users' table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Create the 'tasks' table if it doesn't exist
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    due_date DATETIME NOT NULL,
    alert_date DATETIME NOT NULL,
    description TEXT NOT NULL,
    details TEXT,
    priority TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- The following lines handle sqlite_sequence table creation and initialization
-- Delete existing entries in sqlite_sequence
DELETE FROM sqlite_sequence;

-- Initialize the sequence for 'users' table
INSERT INTO sqlite_sequence VALUES ('users', (SELECT COALESCE(MAX(id)+1, 1) FROM users));

-- Initialize the sequence for 'tasks' table
INSERT INTO sqlite_sequence VALUES ('tasks', (SELECT COALESCE(MAX(id)+1, 1) FROM tasks));

-- Commit the transaction
COMMIT;

-- Turn foreign key constraints back on
PRAGMA foreign_keys=on;

