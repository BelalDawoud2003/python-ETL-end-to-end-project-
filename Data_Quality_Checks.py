import numpy as np
import pandas as pd
import os

# عرض جميع الأعمدة عند الطباعة
pd.set_option('display.max_columns', None)

##################################################
# Products Cleaning & Validation
##################################################
df_products = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\products_extracted.csv")

# Duplicate Check
if df_products.duplicated().sum() > 0:
    df_products.drop_duplicates(inplace=True)
    print("Duplicates found and removed in products_extracted.csv")
else:
    print("No Duplicates in products_extracted.csv")

# product_id validation
valid_product_id = df_products["product_id"] > 0
if valid_product_id.all():
    print("product_id column in products_extracted.csv has valid values")
else:
    df_products = df_products[valid_product_id]
    print("product_id column in products_extracted.csv had invalid values which are removed")

# product_name validation
df_products["product_name"] = df_products["product_name"].replace('', np.nan)
missing_product_names = df_products["product_name"].notnull()
if missing_product_names.all():
    print("product_name column in products_extracted.csv has no missing values")
else:
    df_products = df_products[missing_product_names]
    print("Missing values found and removed in product_name column in products_extracted.csv")

# list_price validation
df_products["list_price"] = df_products["list_price"].replace('', np.nan).astype(float)
missing_list_price = df_products["list_price"].notnull()
if missing_list_price.all():
    print("list_price column in products_extracted.csv has no missing values")
else:
    df_products = df_products[missing_list_price]
    print("Missing values found and removed in list_price column in products_extracted.csv")

# model_year validation
df_products["model_year"] = df_products["model_year"].replace('', np.nan).astype(int)
missing_model_year = df_products["model_year"].notnull() & (df_products["model_year"] > 1950) & (df_products["model_year"] < 2025)
if missing_model_year.all():
    print("model_year column in products_extracted.csv has no missing or invalid values")
else:
    df_products = df_products[missing_model_year]
    print("Missing or invalid values found and removed in model_year column in products_extracted.csv")

# Save cleaned products
df_products.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1\products_cleaned.csv", index=False)
print("Data Quality Checks completed and cleaned data saved for products_extracted.csv")

##################################################
# Customers Cleaning & Validation
##################################################
df_customers = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\customers_extracted.csv")
df_customers.info()

# Drop duplicates
df_customers.drop_duplicates(inplace=True)

# customer_id validation
ch_id = (df_customers["customer_id"] > 0) & (df_customers["customer_id"].duplicated() == False)
if not ch_id.all():
    print("Data Validation Error: 'customer_id' field contains invalid values and not duplicated.")
    print(df_customers[~ch_id][["customer_id"]])
else:
    print("'customer_id' field validation passed successfully.")

# first_name validation
df_customers["first_name"] = df_customers["first_name"].replace(r'^\s*$', np.nan, regex=True)
ch_first_name = df_customers["first_name"].notnull()
if not ch_first_name.all():
    print("Data Validation Error: 'first_name' field contains invalid values.")
    df_customers["first_name"] = df_customers["first_name"].fillna(
        df_customers["email"].str.split('@').str[0].str.split('.').str[0].str.capitalize()
    )
    print(df_customers[~ch_first_name][["customer_id", "first_name", "last_name"]])
else:
    print("'first_name' field validation passed successfully.")

# last_name validation
df_customers["last_name"] = df_customers["last_name"].replace(r'^\s*$', np.nan, regex=True)
ch_last_name = df_customers["last_name"].notnull()
if not ch_last_name.all():
    print("Data Validation Error: 'customer_name' field contains invalid values.")
    df_customers["last_name"] = df_customers["last_name"].fillna(
        df_customers["email"].str.split('@').str[0].str.split('.').str[-1].str.capitalize()
    )
    print(df_customers[~ch_last_name][["customer_id", "first_name", "last_name"]])
else:
    print("'customer_name' field validation passed successfully.")

# phone validation
ch_phone = (df_customers["phone"].str.len() >= 10) & (df_customers["phone"].str.len() <= 15)
if not ch_phone.all():
    print("Data Validation Error: 'phone' field contains invalid values.")
    df_customers["phone"] = df_customers["phone"].fillna("unknown")
    print(df_customers[~ch_phone][["customer_id", "phone"]])
else:
    print("'phone' field validation passed successfully.")

# email validation
ch_email = df_customers["email"].str.contains(
    r"^[a-zA-Z]+\.([a-zA-Z']+)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    na=False
)
if not ch_email.all():
    print("Data Validation Error: 'email' field contains invalid values.")
    df_customers["email"] = df_customers["email"].fillna("unkown")
    print(df_customers[~ch_email][["customer_id", "email"]])
else:
    print("'email' field validation passed successfully.")

# street validation
df_customers["street"] = df_customers["street"].replace(r'^\s*$', np.nan, regex=True)
ch_street = df_customers["street"].notnull()
if not ch_street.all():
    print("Data Validation Error: 'street' field contains invalid values.")
    df_customers["street"] = df_customers["street"].fillna("unknown")
    print(df_customers[~ch_street][["customer_id", "street"]])
else:
    print("'street' field validation passed successfully.")

# city validation
df_customers["city"] = df_customers["city"].replace(r'^\s*$', np.nan, regex=True)
ch_city = df_customers["city"].notnull()
if not ch_city.all():
    print("Data Validation Error: 'city' field contains invalid values.")
    df_customers["city"] = df_customers["city"].fillna("unknown")
    print(df_customers[~ch_city][["customer_id", "city"]])
else:
    print("'city' field validation passed successfully.")

# state validation
df_customers["state"] = df_customers["state"].replace(r'^\s*$', np.nan, regex=True)
ch_state = df_customers["state"].notnull()
if not ch_state.all():
    print("Data Validation Error: 'state' field contains invalid values.")
    df_customers["state"] = df_customers["state"].fillna("unknown")
    print(df_customers[~ch_state][["customer_id", "state"]])
else:
    print("'state' field validation passed successfully.")

# zip_code validation
df_customers["zip_code"] = df_customers["zip_code"].replace(r'^\s*$', np.nan, regex=True)
ch_zip_code = df_customers["zip_code"].notnull()
if not ch_zip_code.all():
    print("Data Validation Error: 'zip_code' field contains invalid values.")
    df_customers["zip_code"] = df_customers["zip_code"].fillna("unknown")
    print(df_customers[~ch_zip_code][["customer_id", "zip_code"]])
else:
    print("'zip_code' field validation passed successfully.")

# Save cleaned customers
df_customers.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1\customers_cleaned.csv", index=False)
print("Data Quality Checks completed and cleaned data saved to staging folder successfully.")

##################################################
# Exchange Rates Cleaning & Validation
##################################################
df_exchange_rates = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\exchange_rates.csv")
df_exchange_rates.drop_duplicates(inplace=True)

# Currency validation
df_exchange_rates['Currency'] = df_exchange_rates['Currency'].replace(r'^\s*$', np.nan, regex=True)
ch_currency = df_exchange_rates['Currency'].notnull()
if not ch_currency.all():
    print("Missing values found in currency column")
    df_exchange_rates['Currency'].fillna('Unknown', inplace=True)
else:
    print("Missing values not found in currency column")

# Rate validation
ch_Rate = df_exchange_rates['Rate'].replace(r'^\s*$', np.nan, regex=True)
ch_Rate = (df_exchange_rates['Rate'].notnull()) & (df_exchange_rates['Rate'] > 0)
if not ch_Rate.all():
    print("Missing values found in Rate column")
    df_exchange_rates['Rate'].fillna(df_exchange_rates['Rate'].mean(), inplace=True)
else:
    print("Missing values not found in Rate column")

# Save cleaned exchange rates
df_exchange_rates.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1\exchange_rates_cleaned.csv", index=False)
##################################################
# Orders Cleaning & Validation
##################################################
df_orders = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\orders.csv")

# Convert dates
df_orders["order_date"] = pd.to_datetime(df_orders["order_date"], errors='coerce')
df_orders["shipped_date"] = pd.to_datetime(df_orders["shipped_date"], errors='coerce')
df_orders["required_date"] = pd.to_datetime(df_orders["required_date"], errors='coerce')
df_orders["extracted_date"] = pd.to_datetime(df_orders["extracted_date"], errors='coerce')

df_orders["data_source"] = df_orders["data_source"].astype(str)
today_date = pd.to_datetime("today")

# Future date check
future_dates = df_orders[(df_orders["order_date"] > today_date) |
                         (df_orders["shipped_date"] > today_date) |
                         (df_orders["required_date"] > today_date)]
if not future_dates.empty:
    print("Data Validation Error: Some date fields contain future dates.")
    print(future_dates[["order_id", "order_date", "shipped_date", "required_date"]])
else:
    print("Date fields validation passed successfully.")

# order_status validation
ch_status = (df_orders["order_status"] > 0) & (df_orders["order_status"] < 5)
if not ch_status.all():
    print("Data Validation Error: 'status' field contains invalid values.")
    print(df_orders[~ch_status][["order_id", "order_status"]])
else:
    print("'status' field validation passed successfully.")

# ID validation
invalid_col = (df_orders["order_id"] > 0) & (df_orders["customer_id"] > 0) & \
              (df_orders["staff_id"] > 0) & (df_orders["store_id"] > 0)
if not invalid_col.all():
    print("Data Validation Error: Some ID fields contain invalid values.")
    print(df_orders[~invalid_col][["order_id", "customer_id", "staff_id", "store_id"]])
else:
    print("ID fields validation passed successfully.")

# data_source validation
invalid_data_source = (df_orders["data_source"].str.strip() != "") & df_orders["data_source"].notnull()
if not invalid_data_source.all():
    print("Data Validation Error: 'data_source' field contains invalid values.")
    print(df_orders[~invalid_data_source][["order_id", "data_source"]])
else:
    print("'data_source' field validation passed successfully.")

# Duplicate check
row_duplicated_number = df_orders.duplicated().sum()
print("number duplicated rows:", row_duplicated_number)
if row_duplicated_number > 0:
    df_orders.drop_duplicates(inplace=True)
    print("duplicated rows found and removed")
else:
    print("no duplicated rows found")

# Null check
df_orders.replace("", np.nan, inplace=True)
null_counts = df_orders.isnull().sum()
if null_counts.any() > 0:
    if df_orders["shipped_date"].isnull().any():
        print("Note: 'shipped_date' column contains null values which may be acceptable if the order has not been shipped yet or canceled.")
    print("Null values found in the dataset.")
    print("Null values in each column:")
    print(null_counts)
else:
    print("No null values found in the dataset.")


##################################################
# Order Items Cleaning & Validation
##################################################
df_orderitems = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\order_items.csv")
df_orderitems["extracted_date"] = pd.to_datetime(df_orderitems["extracted_date"], errors='coerce')

# Data Validation
invalid_col = (df_orderitems["order_id"] > 0) & (df_orderitems["list_price"] >= 0) & \
              (df_orderitems["product_id"] > 0) & (df_orderitems["quantity"] > 0) & (df_orderitems["discount"] >= 0)
if not invalid_col.all():
    print("Data Validation Error: Some fields contain invalid values.")
    print(df_orderitems[~invalid_col][["order_id", "product_id", "quantity", "list_price", "discount"]])
else:
    print("Fields validation passed successfully.")

# Duplicate Check
row_duplicated_number_item = df_orderitems.duplicated().sum()
print("number duplicated rows in order_items:", row_duplicated_number_item)
if row_duplicated_number_item > 0:
    df_orderitems.drop_duplicates(inplace=True)
    print("duplicated rows found and removed in order_items")
else:
    print("no duplicated rows found in order_items")

# Null Check
df_orderitems.replace("", np.nan, inplace=True)
null_count_item = df_orderitems.isnull().sum()
if null_count_item.any() > 0:
    print("Null values found in the order_items dataset.")
    print("Null values in each column:")
    print(null_count_item)
else:
    print("No null values found in the order_items dataset.")


##################################################
# Brands Cleaning & Validation
##################################################
df_brands = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\brands_extracted.csv")
df_brands["extracted_date"] = pd.to_datetime(df_brands["extracted_date"], errors='coerce')

# brand_name validation
invalid_brand_name = (df_brands["brand_name"].str.strip() != "") & (df_brands["brand_name"].notnull())
if not invalid_brand_name.all():
    print("Data Validation Error: 'brand_name' field contains invalid values.")
    print(df_brands[~invalid_brand_name][["brand_id", "brand_name"]])
else:
    print("'brand_name' field validation passed successfully.")

# extracted_date validation
invalid_brand_extracted_date = df_brands["extracted_date"] <= pd.to_datetime("today")
if not invalid_brand_extracted_date.all():
    print("Data Validation Error: 'extracted_date' field contains future dates.")
    print(df_brands[~invalid_brand_extracted_date][["brand_id", "extracted_date"]])
else:
    print("'extracted_date' field validation passed successfully.")

# Duplicate check
row_duplicated_number_brand = df_brands.duplicated().sum()
if row_duplicated_number_brand > 0:
    print("number duplicated rows in brands:", row_duplicated_number_brand)
    df_brands.drop_duplicates(inplace=True)
    print("duplicated rows found and removed in brands")
else:
    print("no duplicated rows found in brands")

# Null check
df_brands.replace("", np.nan, inplace=True)
null_counts_brand = df_brands.isnull().sum()
if null_counts_brand.any() > 0:
    print("Null values found in the brands dataset.")
    print(null_counts_brand)
else:
    print("No null values found in the brands dataset.")
##################################################
# Categories Cleaning & Validation
##################################################
df_categories = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\categories_extracted.csv")
df_categories.info()

# category_id validation
check_id = df_categories["category_id"] > 0
if not check_id.all():
    print("Data Validation Error: 'category_id' field contains invalid values.")
    print(df_categories[~check_id][["category_id", "category_name"]])
else:
    print("'category_id' field validation passed successfully.")

# category_name validation
check_name = (df_categories["category_name"].str.strip() != "") & (df_categories["category_name"].notnull())
if not check_name.all():
    print("Data Validation Error: 'category_name' field contains invalid values.")
    print(df_categories[~check_name][["category_id", "category_name"]])
else:
    df_categories = df_categories.dropna(subset=["category_name"])
    print("'category_name' field validation passed successfully.")

# Duplicate check
row_duplicated_number = df_categories.duplicated().sum()
if row_duplicated_number > 0:
    print("number duplicated rows:", row_duplicated_number)
    df_categories.drop_duplicates(inplace=True)
    print("duplicated rows found and removed")
else:
    print("no duplicated rows found")

# Null check
df_categories.replace("", np.nan, inplace=True)
null_counts = df_categories.isnull().sum()
if null_counts.any() > 0:
    print("Null values found in the dataset.")
    print(null_counts[null_counts > 0])
else:
    print("No null values found in the dataset.")
df_categories["category_name"].fillna("Unknown", inplace=True)


##################################################
# Staffs Cleaning & Validation
##################################################
df_staff = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\staffs_extracted.csv")
df_staff.info()
df_staff.drop_duplicates(inplace=True)

# staff_id validation
ch_staff_id = df_staff['staff_id'] >= 0
if not ch_staff_id.all():
    print("staff_id check failed")
    df_staff = df_staff[ch_staff_id]
else:
    print("staff_id check passed")

# first_name & last_name validation
df_staff["first_name"] = df_staff["first_name"].replace("", np.nan)
df_staff["last_name"] = df_staff["last_name"].replace("", np.nan)
df_staff["first_name"].fillna(df_staff["email"].str.split('@').str[0].str.split('.').str[0].str.capitalize(), inplace=True)
df_staff["last_name"].fillna(df_staff["email"].str.split('@').str[0].str.split('.').str[-1].str.capitalize(), inplace=True)

# email validation
ch_email = df_staff['email'].str.contains(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', na=False)
df_staff.loc[~ch_email, 'email'] = df_staff['first_name'].str.lower() + "." + df_staff['last_name'].str.lower() + "@bikes.shop"

# phone validation
df_staff["phone"] = df_staff["phone"].replace("", np.nan)
ch_phone = df_staff['phone'].str.match(r'^\+?\d{10,15}$', na=False)
df_staff.loc[~ch_phone, 'phone'] = '+0000000000'

# active validation
ch_active = df_staff['active'].isin([0,1])
df_staff.loc[~ch_active, 'active'] = 0

df_staff = df_staff.astype({'manager_id': 'Int64', 'store_id': 'Int64'})
df_staff.info()


##################################################
# Stocks Cleaning & Validation
##################################################
df_stocks = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\stocks_extracted.csv")

# Duplicate check
df_stocks.drop_duplicates(inplace=True)

# store_id, product_id, quantity validation
df_stocks = df_stocks[df_stocks["store_id"] > 0]
df_stocks = df_stocks[df_stocks["product_id"] > 0]
df_stocks["quantity"] = df_stocks["quantity"].replace('', np.nan)
df_stocks = df_stocks[df_stocks["quantity"].notnull() & (df_stocks["quantity"] >= 0)]

# extracted_date validation
df_stocks["extracted_date"] = pd.to_datetime(df_stocks["extracted_date"], errors='coerce')
df_stocks = df_stocks[df_stocks["extracted_date"].notnull()]

# data_source validation
df_stocks["data_source"] = df_stocks["data_source"].replace('', np.nan)
df_stocks = df_stocks[df_stocks["data_source"].notnull()]


##################################################
# Stores Cleaning & Validation
##################################################
df_stores = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\stores_extracted.csv")
df_stores.drop_duplicates(inplace=True)

# Replace empty strings with NaN
for col in ["store_name","email","street","city","state","zip_code"]:
    df_stores[col] = df_stores[col].replace(r'^\s*$', np.nan, regex=True)

# store_name validation
ch_store_name = df_stores["store_name"].notnull()
if not ch_store_name.all():
    print("Data Validation Error: 'store_name' field contains invalid values.")
else:
    print("'store_name' field validation passed successfully.")

# email validation
ch_email = df_stores["email"].str.contains(r"^[a-zA-Z]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", na=False)
df_stores.loc[~ch_email, "email"] = df_stores.loc[~ch_email, "store_name"].str.split().str[0].str.lower() + "@store.shop"

# zip_code cleaning
df_stores["zip_code"] = df_stores["zip_code"].fillna("").astype(str)


##################################################
# Save all cleaned files to staging_1 folder
##################################################
output_path = r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_1"

df_orders.to_csv(os.path.join(output_path, "orders_cleaned.csv"), index=False)
df_orderitems.to_csv(os.path.join(output_path, "order_items_cleaned.csv"), index=False)
df_brands.to_csv(os.path.join(output_path, "brands_cleaned.csv"), index=False)
df_categories.to_csv(os.path.join(output_path, "categories_cleaned.csv"), index=False)
df_staff.to_csv(os.path.join(output_path, "staffs_cleaned.csv"), index=False)
df_stocks.to_csv(os.path.join(output_path, "stocks_cleaned.csv"), index=False)
df_stores.to_csv(os.path.join(output_path, "stores_cleaned.csv"), index=False)

print("\nData Quality Checks completed successfully for all datasets.")
print("Cleaned files saved to staging_1 folder.")
