
CREATE DATABASE IF NOT EXISTS smart_tourism_db;

USE smart_tourism_db;

-- 1. Passenger Table
CREATE TABLE IF NOT EXISTS passengers (
    passenger_id INT PRIMARY KEY,
    route VARCHAR(100),
    travel_date DATE,
    travel_time TIME,
    ticket_price DECIMAL(10,2)
);

-- 2. Hotel Bookings Table
CREATE TABLE IF NOT EXISTS hotel_bookings (
    booking_id INT PRIMARY KEY,
    hotel_name VARCHAR(100),
    customer_name VARCHAR(100),
    check_in DATE,
    check_out DATE,
    room_price DECIMAL(10,2),
    booking_status VARCHAR(30),
    booking_duration INT
);

-- 3. Sales Table
CREATE TABLE IF NOT EXISTS sales (
    transaction_id INT PRIMARY KEY,
    sale_date DATE,
    product VARCHAR(100),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2)
);
