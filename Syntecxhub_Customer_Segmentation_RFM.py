import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

# 1. સેમ્પલ ડેટાસેટ જનરેટ કરવો
np.random.seed(42)
n_rows = 1000

customer_ids = np.random.randint(1001, 1150, size=n_rows)
dates = [dt.datetime(2026, 1, 1) + dt.timedelta(days=int(np.random.randint(0, 280))) for _ in range(n_rows)]
quantities = np.random.randint(1, 10, size=n_rows)
unit_prices = np.random.uniform(10.0, 100.0, size=n_rows).round(2)
invoice_nos = [f"INV{10000 + i}" for i in range(n_rows)]

df = pd.DataFrame({
    'InvoiceNo': invoice_nos,
    'CustomerID': customer_ids,
    'InvoiceDate': dates,
    'Quantity': quantities,
    'UnitPrice': unit_prices
})

# Total Amount
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# 2. RFM કેલ્ક્યુલેશન
latest_date = df['InvoiceDate'].max() + dt.timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (latest_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'TotalAmount': 'sum'
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# 3. RFM સ્કોરિંગ
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])

# 4. કસ્ટમર સેગમેન્ટ નક્કી કરવા
def assign_segment(row):
    r, f = int(row['R_Score']), int(row['F_Score'])
    if r >= 3 and f >= 3:
        return 'Champions / Loyal'
    elif r >= 3 and f < 3:
        return 'New / Potential'
    elif r < 2 and f >= 3:
        return 'At Risk'
    else:
        return 'Lost Customers'

rfm['Segment'] = rfm.apply(assign_segment, axis=1)

# સેગમેન્ટ સેવ કરવું
rfm.to_csv('rfm_segmented_customers.csv', index=False)
print("RFM Analysis Completed!")
print(rfm['Segment'].value_counts())

# 5. ચાર્ટ જનરેટ કરી સેવ કરવો
plt.figure(figsize=(8, 5))
sns.countplot(data=rfm, x='Segment', palette='viridis')
plt.title('Customer Segments Distribution')
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.savefig('rfm_distribution_chart.png')
print("Chart saved as rfm_distribution_chart.png")