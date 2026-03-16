CREATE DATABASE zomato;
USE zomato;
CREATE TABLE customers (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100)
);

CREATE TABLE items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100),
    price DECIMAL(10,2),
    category_id INT
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    delivery_address VARCHAR(255),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT,
    price DECIMAL(10,2)
);

CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    payment_method VARCHAR(50),
    payment_status VARCHAR(50),
    amount DECIMAL(10,2)
);

INSERT INTO categories(category_name) VALUES
('Vegetarian'),
('Non-Vegetarian');

INSERT INTO items(item_name,price,category_id) VALUES
('Biriyani',150,2),
('Paneer Butter Masala',120,1),
('Butter Chicken',200,2),
('Veg Fried Rice',100,1),
('Chicken Noodles',130,2);