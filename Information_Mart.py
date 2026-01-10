import mysql.connector
import pandas as pd
import os

# تحديد مسار المجلد
output_dir = r"C:\Users\Belal\Desktop\Etman\projects\project_python\information_mart"
os.makedirs(output_dir, exist_ok=True)  # إنشاء المجلد لو مش موجود

# الاتصال بقاعدة البيانات
con = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='12qq12ww12ee',
    database='project_py_DWH'
)

# ================== Region ==================
query_region = "SELECT * FROM region"
df_region = pd.read_sql(query_region, con)
print(df_region.head())
df_region.to_csv(os.path.join(output_dir, "region.csv"), index=False)

# ================== Product ==================
query_product = "SELECT * FROM product"
df_product = pd.read_sql(query_product, con)
print(df_product.head())
df_product.to_csv(os.path.join(output_dir, "product.csv"), index=False)

# ================== Brands ==================
query_brands = "SELECT * FROM Brands"
df_brands = pd.read_sql(query_brands, con)
print(df_brands.head())
df_brands.to_csv(os.path.join(output_dir, "brands.csv"), index=False)

# ================== Categories ==================
query_categories = "SELECT * FROM categories"
df_categories = pd.read_sql(query_categories, con)
print(df_categories.head())
df_categories.to_csv(os.path.join(output_dir, "categories.csv"), index=False)

# ================== Customers ==================
query_customers = "SELECT * FROM customers"
df_customers = pd.read_sql(query_customers, con)
print(df_customers.head())
df_customers.to_csv(os.path.join(output_dir, "customers.csv"), index=False)

# ================== Staffs ==================
query_staffs = "SELECT * FROM staffs"
df_staffs = pd.read_sql(query_staffs, con)
print(df_staffs.head())
df_staffs.to_csv(os.path.join(output_dir, "staffs.csv"), index=False)

# ================== Stores ==================
query_stores = "SELECT * FROM stores"
df_stores = pd.read_sql(query_stores, con)
print(df_stores.head())
df_stores.to_csv(os.path.join(output_dir, "stores.csv"), index=False)

# ================== Dim Date ==================
query_dim_date = "SELECT * FROM dim_date"
df_dim_date = pd.read_sql(query_dim_date, con)
print(df_dim_date.head())
df_dim_date.to_csv(os.path.join(output_dir, "dim_date.csv"), index=False)

# ================== Order Status ==================
query_order_status = "SELECT * FROM order_status"
df_order_status = pd.read_sql(query_order_status, con)
print(df_order_status.head())
df_order_status.to_csv(os.path.join(output_dir, "order_status.csv"), index=False)

# ================== Fact Sales ==================
query_fact_sales = "SELECT * FROM fact_sales"
df_fact_sales = pd.read_sql(query_fact_sales, con)
print(df_fact_sales.head())
df_fact_sales.to_csv(os.path.join(output_dir, "fact_sales.csv"), index=False)
