import mysql.connector
from datetime import datetime, timedelta

# ===== إعداد الاتصال بقاعدة البيانات =====
con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12qq12ww12ee',
    database='project_py_DWH'
)
cursor = con.cursor()

# ===== إعداد الفترة الزمنية =====
start_year = 1950
end_year = 2035

start_date = datetime(start_year, 1, 1)
end_date = datetime(end_year, 12, 31)

# ===== إدخال التواريخ يوم بيوم =====
batch_size = 1000
count = 0

current_date = start_date
while current_date <= end_date:
    day = current_date.day
    month = current_date.month
    month_name = current_date.strftime('%B')
    quarter = f"Q{((month-1)//3)+1}"
    year = current_date.year
    weekday = current_date.strftime('%A')
    is_weekend = 1 if weekday in ['Saturday', 'Sunday'] else 0
    date_id = year * 10000 + month * 100 + day

    cursor.execute("""
        INSERT INTO dim_date (date_id, full_date, day, month, month_name, quarter, year, weekday, is_weekend)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (date_id, current_date.strftime('%Y-%m-%d'), day, month, month_name, quarter, year, weekday, is_weekend))

    count += 1
    if count % batch_size == 0:
        con.commit()  # commit كل 1000 صف

    current_date += timedelta(days=1)

con.commit()  # commit النهائي

cursor.close()
con.close()

print(f"dim_date table populated successfully for {start_year} to {end_year}!")
