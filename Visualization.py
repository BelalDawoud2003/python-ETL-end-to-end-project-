import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# الاتصال بقاعدة البيانات
con = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='12qq12ww12ee',
    database='project_py_DWH'
)

# إنشاء Cursor لتنفيذ الاستعلامات
cursor = con.cursor()

# مثال: قراءة جدول كامل إلى DataFrame
query = """select sum(total_amount_EG) as sum_total_amount_EG,r.city
	from fact_sales f join region r 
	on f.region_id=r.region_id
	group by r.city
	order by  sum_total_amount_EG desc 
    limit 10;

"""
query_1 = """select f.product_id,p.product_name ,sum(quantity) as sum_total_quantity
from fact_sales f join product p
on f.product_id=p.pro_id
group by f.product_id
order by sum_total_quantity desc 
limit 10 ;
"""

query_2 = """select  sum(total_amount_EG) as sum_total_amount_EG ,first_name,last_name, c.customer_id
from fact_sales f join customers c
on f.customer_id=c.customer_id
group by c.customer_id
order by  sum_total_amount_EG desc ;
"""
query_3 = """select sum(total_amount_EG) ,sum(quantity), month, year
from fact_sales f join dim_date d
on f.order_date=d.date_id
group by month, year;
"""
df = pd.read_sql(query, con)
df_1=pd.read_sql(query_1,con)
df_2=pd.read_sql(query_2,con)
df_3=pd.read_sql(query_3,con)
print(df.head())
print(df_1.head())
print(df_2.head())
print(df_3.head())
# غلق الاتصال بعد الانتهاء
con.close()


import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 1️⃣ رسم بياني لمجموع المبيعات حسب المدينة (Bar chart)
plt.figure(figsize=(10,6))
sns.barplot(x='city', y='sum_total_amount_EG', data=df, palette='viridis')
plt.title("Total Sales per City", fontsize=16, fontweight='bold')
plt.xlabel("City", fontsize=14)
plt.ylabel("Total Sales (EGP)", fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Plotly version (تفاعلي)
fig1 = px.bar(df, x='city', y='sum_total_amount_EG', 
              title='Total Sales per City', 
              labels={'sum_total_amount_EG':'Total Sales (EGP)','city':'City'},
              color='sum_total_amount_EG',
              color_continuous_scale='Viridis')
fig1.show()


# 2️⃣ أفضل 10 منتجات حسب الكمية المباعة (Horizontal Bar Chart)
plt.figure(figsize=(10,6))
sns.barplot(x='sum_total_quantity', y='product_name', data=df_1, palette='magma')
plt.title("Top 10 Products by Quantity Sold", fontsize=16, fontweight='bold')
plt.xlabel("Total Quantity Sold", fontsize=14)
plt.ylabel("Product Name", fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Plotly version
fig2 = px.bar(df_1, x='sum_total_quantity', y='product_name', orientation='h',
              title='Top 10 Products by Quantity Sold',
              labels={'sum_total_quantity':'Total Quantity','product_name':'Product Name'},
              color='sum_total_quantity', color_continuous_scale='Magma')
fig2.show()


# 3️⃣ أفضل العملاء حسب المبيعات (Bar Chart)
plt.figure(figsize=(12,6))
df_2['customer_name'] = df_2['first_name'] + ' ' + df_2['last_name']
sns.barplot(x='customer_name', y='sum_total_amount_EG', data=df_2.head(10), palette='coolwarm')
plt.title("Top 10 Customers by Total Sales", fontsize=16, fontweight='bold')
plt.xlabel("Customer", fontsize=14)
plt.ylabel("Total Sales (EGP)", fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Plotly version
fig3 = px.bar(df_2.head(10), x='customer_name', y='sum_total_amount_EG', 
              title='Top 10 Customers by Total Sales',
              labels={'sum_total_amount_EG':'Total Sales (EGP)','customer_name':'Customer'},
              color='sum_total_amount_EG', color_continuous_scale='RdBu')
fig3.show()


# 4️⃣ المبيعات والكمية حسب الشهر والسنة (Line Chart)
plt.figure(figsize=(12,6))
sns.lineplot(data=df_3, x='month', y='sum(total_amount_EG)', hue='year', marker='o', palette='tab10')
plt.title("Monthly Sales by Year", fontsize=16, fontweight='bold')
plt.xlabel("Month", fontsize=14)
plt.ylabel("Total Sales (EGP)", fontsize=14)
plt.xticks(range(1,13))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Plotly version
fig4 = px.line(df_3, x='month', y='sum(total_amount_EG)', color='year', markers=True,
               title='Monthly Sales by Year',
               labels={'sum(total_amount_EG)':'Total Sales (EGP)','month':'Month','year':'Year'},
               line_shape='spline')
fig4.show()

