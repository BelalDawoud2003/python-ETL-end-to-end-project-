import pandas as pd
from datetime import datetime

stores_df = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\file\stores.csv")
stores_df["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
stores_df["data_source"]= "from_csv_file"
stores_df.to_csv("extraction/stores_extracted.csv", index=False)   
categories_df = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\file\categories.csv")
categories_df["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
categories_df["data_source"]= "from_csv_file"   
categories_df.to_csv("extraction/categories_extracted.csv", index=False)
customers_df = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\file\customers.csv")
customers_df["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
customers_df["data_source"]= "from_csv_file"    
customers_df.to_csv("extraction/customers_extracted.csv", index=False)
brands_df = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\file\brands.csv")
brands_df["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
brands_df["data_source"]= "from_csv_file"
brands_df.to_csv("extraction/brands_extracted.csv", index=False)
products_df = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\file\products.csv")
products_df["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
products_df["data_source"]= "from_csv_file" 
products_df.to_csv("extraction/products_extracted.csv", index=False)
staffs_df = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\file\staffs.csv")
staffs_df["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
staffs_df["data_source"]= "from_csv_file"   
staffs_df.to_csv("extraction/staffs_extracted.csv", index=False)
stocks_df = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\extraction\file\stocks.csv")
stocks_df["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
stocks_df["data_source"]= "from_csv_file"   
stocks_df.to_csv("extraction/stocks_extracted.csv", index=False)
print("Data extracted and saved successfully.")

