-- CUISINE TEST SET UP
CREATE DATABASE IF NOT EXISTS cuisine_test_db;
CREATE USER IF NOT EXISTS 'cuisine_test'@'localhost' IDENTIFIED BY 'cuisine_test_pwd';
GRANT ALL PRIVILEGES ON cuisine_test_db . * TO 'cuisine_test'@'localhost';
GRANT SELECT ON perfomance_schema . * TO 'cuisine_test'@'localhost';
