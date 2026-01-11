import numpy as np
import pandas as pd
import os

pd.set_option('display.max_columns', None)

# =========================
# Products & Currency Conversion
# =========================
df_products = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/products_cleaned.csv")
df_exchange_rates = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/exchange_rates_cleaned.csv")

df_egp = df_exchange_rates[df_exchange_rates["Currency"] == "EGP"]
rate = df_egp["Rate"].iloc[0]

df_products["local_price"] = df_products["list_price"] * rate

df_order_item = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/order_items_cleaned.csv")
df_order_item["local_price"] = df_order_item["list_price"] * rate

print(df_order_item.head())

df_products.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/product.csv")
df_order_item.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/order_item.csv")

# =========================
# Orders Processing
# =========================
df_orders = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/orders_cleaned.csv")
df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])
df_orders["required_date"] = pd.to_datetime(df_orders["required_date"])
df_orders["shipped_date"] = pd.to_datetime(df_orders["shipped_date"])
df_orders["latency_days"] = (df_orders["shipped_date"] - df_orders["order_date"]).dt.days
df_orders["Late_Deliveries:"] = (df_orders["shipped_date"] > df_orders["required_date"])

# =========================
# Customers & Stores
# =========================
df_customers = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/customers_cleaned.csv")
df_store = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/stores_cleaned.csv")

df_orders = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/orders_cleaned.csv")
df_orders["order_date"] = pd.to_datetime(df_orders["order_date"])
df_orders["required_date"] = pd.to_datetime(df_orders["required_date"])
df_orders["shipped_date"] = pd.to_datetime(df_orders["shipped_date"])
df_orders["latency_days"] = (df_orders["shipped_date"] - df_orders["order_date"]).dt.days
df_orders["Late_Deliveries:"] = (df_orders["shipped_date"] > df_orders["required_date"])

df_store["zip_code"] = df_store["zip_code"].astype(str)
df_store["zip_code"] = df_store["zip_code"].str.replace(r"\.0$", "", regex=True)

# =========================
# Merge Orders with Customers & Stores
# =========================
df_orders_customers = df_orders.merge(df_customers, on="customer_id", how="left")
df_orders_customers_store = df_orders_customers.merge(df_store, on="store_id", how="left")

df_orders["Locality_Flag"] = df_orders_customers_store.apply(
    lambda row: "local" if row["city_x"] == row["city_y"] else "Non local",
    axis=1
)

# =========================
# Add Order Status Names
# =========================
df_statuses = pd.DataFrame({
    'order_status': [1, 2, 3, 4],
    'order_status_name': ['ordered', 'Completed', 'Cancelled', 'Shipped']
})

df_statuses_order = df_orders.merge(df_statuses, on="order_status", how="left")

df_statuses.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/order_status.csv")
df_orders.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/orders.csv")

# =========================
# Export Other Tables (Same Code, Preserved 100%)
# =========================
df_customers = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/customers_cleaned.csv")
df_customers.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/customers.csv")

df_brands = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/brands_cleaned.csv")
df_brands.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/brands.csv")

df_categories = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/categories_cleaned.csv")
df_categories.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/categories.csv")

df_exchange_rates = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/exchange_rates_cleaned.csv")
df_exchange_rates.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/exchange_rates.csv")

df_staff = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/staffs_cleaned.csv")
df_staff.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/staffs.csv")

df_stocks = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/stocks_cleaned.csv")
df_stocks.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/stocks.csv")

df_store = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1/stores_cleaned.csv")
df_store.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/stores.csv")

print(df_orders.head())