import mysql.connector 
from mysql.connector import Error
import pandas as pd
from datetime import datetime

try :
    conn= mysql.connector.connect(
        host='localhost',  
        port =3306,
        user ='root',
        password ='12qq12ww12ee',
        database ='project'  
    )   
    if conn.is_connected():
        print("Connection to the database was successful.") 
        order_df = pd.read_sql("SELECT * FROM orders", conn)
        order_df["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_df["data_source"]= "mysql_database"
        print(order_df.head())
        order_df.to_csv("extraction/orders.csv", index=False)
        print("Orders data saved to 'extraction/orders.csv'")
        item_df = pd.read_sql("SELECT * FROM order_items", conn)
        item_df["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item_df["data_source"]= "mysql_database"
        print(item_df.head())
        item_df.to_csv("extraction/order_items.csv", index=False)
        print("Order items data saved to 'extraction/order_items.csv'")
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if conn.is_connected():
        conn.close()
        print("MySQL connection is closed.")    

     