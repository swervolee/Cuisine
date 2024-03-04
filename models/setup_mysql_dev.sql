-- CUISINE DATABASE SET UP
CREATE DATABASE IF NOT EXISTS cuisine_dev_db;
CREATE USER IF NOT EXISTS 'cuisine_dev'@'localhost' IDENTIFIED BY 'cuisine_dev_pwd';
GRANT ALL PRIVILEGES ON cuisine_dev_db.* TO 'cuisine_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'cuisine_dev'@'localhost';
