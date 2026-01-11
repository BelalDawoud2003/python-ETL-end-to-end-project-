import pandas as pd
import requests
from datetime import datetime
api_url = "https://openexchangerates.org/api/latest.json"
api_key = "537eeee49d874dcbaacfd73734c6dd43"

response = requests.get(api_url,params={"app_id": api_key})
if response.status_code == 200:
    data =response.json()
    print(" Data fetched successfully!")
else :
    print(" Failed to fetch data:", response.status_code)
    data = {}
if "rates" in data:
    rates =data["rates"]
    df=pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"])
    df["extracted_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df["data_source"]= "openexchangerates_api"
    print(df.head())
else:
    df=pd.DataFrame()
    print(" 'rates' key not found in the response data.")
df.to_csv("extraction/exchange_rates.csv", index=False)
print(" Exchange rates saved to 'extraction/exchange_rates.csv'")
