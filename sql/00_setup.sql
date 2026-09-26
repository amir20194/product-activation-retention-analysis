-- Run in an empty MySQL 8 database before importing the CSV files.
-- Dates in users.csv and events.csv are ISO formatted.

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    signup_date DATETIME NOT NULL,
    country VARCHAR(50) NOT NULL,
    platform VARCHAR(20) NOT NULL,
    acquisition_channel VARCHAR(50) NOT NULL
);

CREATE TABLE events (
    user_id INT NOT NULL,
    event_timestamp DATETIME NOT NULL,
    event_name VARCHAR(50) NOT NULL,
    INDEX (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
