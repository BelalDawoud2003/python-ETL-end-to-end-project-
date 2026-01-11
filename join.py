import numpy as np
import pandas as pd
import mysql.connector

pd.set_option('display.max_columns', None)

# =========================
# قراءة ملفات CSV
# =========================
df_brand = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/brands.csv")
df_categories = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/categories.csv")
df_customers = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/customers.csv")
df_staffs = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/staffs.csv")
df_order_status = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/order_status.csv")
df_stores = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/stores.csv")
df_product = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/product.csv")
df_orders = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/orders.csv")
df_order_item = pd.read_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/order_item.csv")

# =========================
# معالجة القيم الفارغة
# =========================
df_staffs['manager_id'] = df_staffs['manager_id'].where(pd.notnull(df_staffs['manager_id']), None)

# إنشاء df_region من العملاء والمتاجر وإزالة التكرارات
df_region = df_customers[['city', 'state']].copy()

# إزالة التكرارات
df_region.drop_duplicates(inplace=True)

# إضافة عمود region_id يبدأ من 1
df_region.insert(0, 'region_id', range(1, len(df_region) + 1))
df_region.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/region.csv")



# معالجة zip_code
df_stores['zip_code'] = (
    df_stores['zip_code']
    .astype(str)
    .str.replace('.0', '', regex=False)
    .replace('nan', None)
)

# =========================
# دمج الجداول مع suffixes لتجنب الأعمدة المكررة
# =========================
df_join = pd.merge(
    df_orders,
    df_order_item,
    on='order_id',
    how='inner',
    suffixes=('_order', '_order_item')
)

df_join = pd.merge(
    df_join,
    df_order_status,
    on='order_status',
    how='inner',
    suffixes=('_order', '_status')
)

df_join = pd.merge(
    df_join,
    df_customers,
    on='customer_id',
    how='inner',
    suffixes=('', '_customer')
)

df_join = pd.merge(
    df_join,
    df_product,
    on='product_id',
    how='inner',
    suffixes=('', '_product')
)

df_join = pd.merge(
    df_join,
    df_brand,
    on='brand_id',
    how='inner',
    suffixes=('', '_brand')
)

df_join = pd.merge(
    df_join,
    df_categories,
    on='category_id',
    how='inner',
    suffixes=('', '_category')
)

df_join = pd.merge(
    df_join,
    df_stores,
    on='store_id',
    how='inner',
    suffixes=('', '_store')
)

# إعادة تسمية أعمدة staffs لتجنب التعارض
df_staffs = df_staffs.rename(columns={
    'data_source': 'data_source_staff',
    'extracted_date': 'extracted_date_staff'
})

df_join = pd.merge(
    df_join,
    df_staffs,
    on='staff_id',
    how='inner',
    suffixes=('', '_staff')
)
df_join = pd.merge(
    df_join,
    df_region,
    on=['city', 'state'],
    how='inner',
    suffixes=('', '_region')
)


df_join['total_amount_US'] = np.where(
    df_join['discount'] > 0,
    df_join['discount'] * df_join['list_price'] * df_join['quantity'],
    df_join['list_price'] * df_join['quantity']
)
df_join['total_amount_EG'] = np.where(
    df_join['discount'] > 0,
    df_join['discount'] * df_join['local_price'] * df_join['quantity'],
    df_join['local_price'] * df_join['quantity']
)
# =========================
# اختيار الأعمدة النهائية
# =========================

columns_to_select = [
    'order_id', 'item_id', 'order_status', 'customer_id',
    'product_id', 'brand_id', 'category_id', 'store_id', 
    'staff_id', 'order_date', 'required_date', 'shipped_date','region_id','latency_days','Late_Deliveries','Locality_Flag','quantity','list_price','local_price',
    'discount','total_amount_US','total_amount_EG'
]
df_join = df_join.rename(columns={'Late_Deliveries:': 'Late_Deliveries'})
# تحويل order_date إلى int بصيغة YYYYMMDD
df_join['order_date'] = pd.to_datetime(df_join['order_date'], errors='coerce')
df_join['order_date'] = df_join['order_date'].dt.strftime('%Y%m%d').astype('Int64')

# نفس الشيء للـ required_date و shipped_date لو موجودين
df_join['required_date'] = pd.to_datetime(df_join['required_date'], errors='coerce')
df_join['required_date'] = df_join['required_date'].dt.strftime('%Y%m%d').astype('Int64')

df_join['shipped_date'] = pd.to_datetime(df_join['shipped_date'], errors='coerce')
df_join['shipped_date'] = df_join['shipped_date'].dt.strftime('%Y%m%d').astype('Int64')

df_fil = df_join[columns_to_select]
# =========================
# حفظ النتائج
# =========================
df_fil.drop_duplicates()
#df_join.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/join2.csv", index=False)
df_fil.to_csv(r"C:\Users\Belal\Desktop\Etman\projects\project_python\staging_2/join.csv", index=False)

# =========================
# التحقق من الأعمدة المكررة
# =========================
print(df_fil.columns.tolist())
