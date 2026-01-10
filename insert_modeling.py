import numpy as np
import pandas as pd
import os
import mysql.connector  
pd.set_option('display.max_columns', None)
df_brand=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/brands.csv")
df_categories=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/categories.csv")
df_customers=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/customers.csv")
df_staffs=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/staffs.csv")
df_order_status=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/order_status.csv")
df_stores=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/stores.csv")
df_product=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/product.csv")
df_orders=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/orders.csv")
df_order_item=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/order_item.csv")
df_region=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/region.csv")
df_join=pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/join.csv")

# استبدل NaN بقيمة افتراضية حسب نوع العمود
df_staffs['manager_id'] = df_staffs['manager_id'].where(pd.notnull(df_staffs['manager_id']), None)

df_stores['zip_code'] = (
    df_stores['zip_code']
    .astype(str)              # حوله لنص
    .str.replace('.0', '', regex=False)   # شيل .0
    .replace('nan', None)     # لو فيه قيم NaN
)
try:
    con=mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='12qq12ww12ee',
        database='project_py_DWH'
    )
    cursor=con.cursor()
    
    cursor.executemany(
    "INSERT INTO Brands (brand_id, brand_name) VALUES (%s, %s)",
    [tuple(row) for row in df_brand[['brand_id', 'brand_name']].values]
    )
    # إدخال Categories
    cursor.executemany(
    "INSERT INTO Categories (category_id, category_name) VALUES (%s, %s)",
    [tuple(row) for row in df_categories[['category_id', 'category_name']].values]
    )
    cursor.executemany(
    "INSERT INTO customers (customer_id,first_name,last_name,phone,email,street,city,state,zip_code) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)",
    [tuple(row) for row in df_customers[['customer_id', 'first_name','last_name','phone','email','street','city','state','zip_code']].values]
    )
    cursor.executemany(
    "INSERT INTO staffs (staff_id, first_name, last_name, email, active, manager_id) VALUES (%s,%s,%s,%s,%s,%s)",
    [tuple(x) for x in df_staffs[['staff_id','first_name','last_name','email','active','manager_id']].fillna(value=np.nan).replace({np.nan: None}).values]
    )
    cursor.executemany(
    "INSERT INTO order_status (order_status, order_status_name) VALUES (%s, %s)",
    [tuple(row) for row in df_order_status[['order_status', 'order_status_name']].values]
    )

    cursor.executemany(
    "INSERT INTO stores (store_id, store_name, phone, email, street, city,state,zip_code) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
    [tuple(x) for x in df_stores[['store_id', 'store_name', 'phone', 'email', 'street', 'city','state','zip_code']].fillna(value=np.nan).replace({np.nan: None}).values]
    )
    cursor.executemany(
    "INSERT INTO product (pro_id, product_name, model_year, list_price, list_local_price) VALUES (%s,%s,%s,%s,%s)",
    [tuple(x) for x in df_product[['product_id', 'product_name', 'model_year', 'list_price','local_price']].fillna(value=np.nan).replace({np.nan: None}).values]
    )
    cursor.executemany(
        "INSERT INTO region ( region_id,city, state) VALUES (%s, %s,%s)",
        [tuple(x) for x in df_region[[ 'region_id','city', 'state']].values]
    )
# تحويل DataFrame إلى list of tuples مع استبدال np.nan بـ None
    data_to_insert = [
    tuple(None if pd.isna(x) else x for x in row)
    for row in df_join.values
    ]
    cursor.executemany(
    """
    INSERT INTO fact_sales (
        order_id, item_id, order_status, customer_id,
        product_id, brand_id, category_id, store_id,
        staff_id, order_date, required_date, shipped_date,
        region_id, latency_days, Late_Deliveries,
        Locality_Flag, quantity, list_price, local_price,
        discount, total_amount_US, total_amount_EG
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
    data_to_insert
    )


    con.commit()
    #cursor.executemany(

    #)
    # 🔹 غلق cursor والاتصال
    cursor.close()
    con.close()

except mysql.connector.Error as e:
    print(f"error: {e}")