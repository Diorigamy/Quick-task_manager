-- schema.sql

PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

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
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES ('users', (SELECT COALESCE(MAX(id)+1, 1) FROM users));
INSERT INTO sqlite_sequence VALUES ('tasks', (SELECT COALESCE(MAX(id)+1, 1) FROM tasks));

COMMIT;
PRAGMA foreign_keys=on;

