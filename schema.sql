-- Drop tables if they already exist to start fresh
DROP TABLE IF EXISTS "transaction";
DROP TABLE IF EXISTS monthly_transaction;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS "user";

-- Create User Table
CREATE TABLE "user" (
    u_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create Category Table
CREATE TABLE category (
    c_id VARCHAR(50) PRIMARY KEY,
    c_name VARCHAR(50) NOT NULL,
    c_desc VARCHAR(200),
    c_goal REAL,
    is_custom BOOLEAN DEFAULT 0
);

-- Create Monthly Transaction Table (with Composite Key)
CREATE TABLE monthly_transaction (
    month INTEGER,
    year INTEGER,
    month_goal REAL,
    last_updated DATE,
    PRIMARY KEY (month, year)
);

-- Create Transaction Table
CREATE TABLE "transaction" (
    t_id VARCHAR(50) PRIMARY KEY,
    u_id VARCHAR(50) NOT NULL,
    c_id VARCHAR(50) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    vendor_name VARCHAR(100),
    purchase_date DATETIME NOT NULL,
    t_amount REAL NOT NULL,
    payment_method VARCHAR(50),
    FOREIGN KEY (u_id) REFERENCES "user" (u_id),
    FOREIGN KEY (c_id) REFERENCES category (c_id)
);