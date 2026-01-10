import numpy as np
import pandas as pd
import os
import mysql.connector  
# عرض جميع الأعمدة عند الطباعة
#pd.set_option('display.max_columns', None)
try:
    conn=mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='12qq12ww12ee',
        database='project_py_DWH'
    )
    cursor=conn.cursor()
    query=""" 
CREATE TABLE IF NOT EXISTS product (
    pro_id INT UNSIGNED NOT NULL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    model_year INT NOT NULL,
    list_price DECIMAL(10,2) NOT NULL,
    list_local_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE Brands (
    brand_id INT UNSIGNED NOT NULL PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL
);

CREATE TABLE categories (
    category_id INT UNSIGNED NOT NULL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);

CREATE TABLE customers (
    customer_id INT UNSIGNED NOT NULL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone VARCHAR(255),
    email VARCHAR(255),
    street VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zip_code VARCHAR(255)
);

CREATE TABLE staffs (
    staff_id INT UNSIGNED NOT NULL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone VARCHAR(255),
    email VARCHAR(255),
    active INT,
    manager_id FLOAT
);

CREATE TABLE stores (
    store_id INT UNSIGNED NOT NULL PRIMARY KEY,
    store_name VARCHAR(255) NOT NULL,
    phone VARCHAR(255),
    email VARCHAR(255),
    street VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zip_code VARCHAR(255)
);

CREATE TABLE dim_date (
    date_id INT UNSIGNED NOT NULL PRIMARY KEY,
    full_date DATE NOT NULL,
    day INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(50) NOT NULL,
    quarter VARCHAR(50) NOT NULL,
    year INT,
    weekday VARCHAR(50) NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

CREATE TABLE order_status (
    order_status INT UNSIGNED NOT NULL PRIMARY KEY,
    order_status_name VARCHAR(255) NOT NULL
);

CREATE TABLE region (
    region_id INT UNSIGNED NOT NULL PRIMARY KEY,
    city VARCHAR(255),
    state VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS fact_sales (
    order_item_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    order_status INT UNSIGNED NOT NULL,
    brand_id INT UNSIGNED NOT NULL,
    customer_id INT UNSIGNED NOT NULL,
    category_id INT UNSIGNED NOT NULL,
    store_id INT UNSIGNED NOT NULL,
    staff_id INT UNSIGNED NOT NULL,
    product_id INT UNSIGNED NOT NULL,
    required_date INT UNSIGNED,
    shipped_date INT UNSIGNED,
    order_date INT UNSIGNED NOT NULL,
    region_id INT UNSIGNED,
    latency_days FLOAT,
    Late_Deliveries BOOLEAN,
    Locality_Flag VARCHAR(50),
    quantity INT NOT NULL,
    list_price DECIMAL(10,2) NOT NULL,
    local_price DECIMAL(10,2) NOT NULL,
    discount FLOAT,
    total_amount_US DECIMAL(10,2) NOT NULL,
    total_amount_EG DECIMAL(10,2) NOT NULL,
    FOREIGN KEY(order_status_id) REFERENCES order_status(order_status_id),
    FOREIGN KEY(required_date) REFERENCES dim_date(date_id),
    FOREIGN KEY(staff_id) REFERENCES staffs(staff_id),
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(shipped_date) REFERENCES dim_date(date_id),
    FOREIGN KEY(region_id) REFERENCES region(region_id),
    FOREIGN KEY(category_id) REFERENCES categories(category_id),
    FOREIGN KEY(product_id) REFERENCES product(pro_id),
    FOREIGN KEY(store_id) REFERENCES stores(store_id),
    FOREIGN KEY(brand_id) REFERENCES Brands(brand_id),
    FOREIGN KEY(order_date) REFERENCES dim_date(date_id)
);

);

    """
    cursor.execute(query)
    cursor.close()
    conn.close()
except mysql.connector.Error as e:
    print(f"error: {e}")
























































































 #results=cursor.fetchall()
    #print(cursor.description)
    #column_name=[desc[0] for desc in cursor.description]
    #print(" | ".join(column_name))