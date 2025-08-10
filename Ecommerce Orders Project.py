# -*- coding: utf-8 -*-
"""
@author: MinhTok1oPC

Question:
    - The investors would want to see the range of payments amounts by payment type(like credit cards, debit cards)
    - The investors want to see payment values by payment type for everymonth
    - They would like to see the totals payments values by month
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('D:/Py-Material/Ecommerce+Orders+Project/Ecommerce Orders Project')
print(os.getcwd())


orders_data = pd.read_excel('orders.xlsx')
payments_data = pd.read_excel('order_payment.xlsx')
customers_data = pd.read_excel('customers.xlsx')

#orders_data.info()
#payments_data.info()
#customers_data.info()

#=========================================
# Handling data
#=========================================
orders_data.isnull().sum()
payments_data.isnull().sum()
customers_data.isnull().sum()

#with orders_data, fill any missing value with default value
orders_data = orders_data.fillna('N/A')
orders_data.isnull().sum()

#with payment_data, drop rows with missing values
payments_data = payments_data.dropna()
payments_data.isnull().sum()

#Remove duplicated data
orders_data = orders_data.drop_duplicates()
orders_data.duplicated().sum()

payments_data = payments_data.drop_duplicates()
payments_data.duplicated().sum()

#=========================================
# Filtering data
#=========================================
# Subset of orders data based on the order status
status_orders = orders_data[orders_data['order_status'] == 'invoiced']
status_orders = status_orders.reset_index(drop = True)

#Subset of payments data where payment type = Credit card & payment value > 1000
credit_payments = payments_data[(payments_data['payment_type'] == 'credit_card') & (payments_data['payment_value'] > 1000)]

#Subset of customers based on customer state = SP
sp_customers = customers_data[customers_data['customer_state'] == 'SP']

#=========================================
# Merge data
#=========================================
merge_data = pd.merge(orders_data, payments_data, on = 'order_id')
full_join_data = pd.merge(merge_data, customers_data, on = 'customer_id')

#=========================================
# Data Visualization
#=========================================
# Create X and Y for matplot
full_join_data['month_year'] = full_join_data['order_purchase_timestamp'].dt.to_period('M')
full_join_data['week_year'] = full_join_data['order_purchase_timestamp'].dt.to_period('W')
full_join_data['year'] = full_join_data['order_purchase_timestamp'].dt.to_period('Y')

total_payments_per_month = full_join_data.groupby('month_year')['payment_value'].sum()
total_payments_per_month = total_payments_per_month.reset_index()

#Convert month_year from period to string
total_payments_per_month['month_year'] = total_payments_per_month['month_year'].astype(str)

#Create plot
plt.plot(total_payments_per_month['month_year'], total_payments_per_month['payment_value'], marker = 'o')
plt.ticklabel_format(useOffset = False, style = 'plain', axis = 'y')
plt.xlabel('Month and Year')
plt.ylabel('Payment Value')
plt.title('Payment Values By Month')
plt.xticks(rotation = 90, fontsize = 8)
plt.yticks(fontsize = 8)

#Create payment installments plot vs payment values based on customers
scatter_df = full_join_data.groupby('customer_unique_id').agg({'payment_value' : 'sum', 'payment_installments' : 'sum'})
sns.set_theme(style = 'darkgrid')
sns.scatterplot(data = scatter_df, x = 'payment_value', y = 'payment_installments')
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment Values vs Payment Installments')

#Create payments values based on payment type over the year (month_year)
bar_chart_df = full_join_data.groupby(['payment_type', 'month_year'])['payment_value'].sum()
bar_chart_df = bar_chart_df.reset_index()

pivot_data = bar_chart_df.pivot(index = 'month_year', columns = 'payment_type', values = 'payment_value')

pivot_data.plot(kind = 'bar', stacked = 'True')
plt.ticklabel_format(useOffset = False, style = 'plain', axis = 'y')
plt.xlabel('Month')
plt.ylabel('Payment')
plt.title('Payment Values per Payment Type by Month')

#Create payments values for each type of payment type
payment_values = full_join_data['payment_value']
payment_types = full_join_data['payment_type']

plt.boxplot([payment_values[payment_types == 'credit_card'],
             payment_values[payment_types == 'boleto'],
             payment_values[payment_types == 'voucher'],
             payment_values[payment_types == 'debit_card']],
            labels = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
           )
plt.xlabel('Payment Type')
plt.ylabel('Payment Value')
plt.title('Payment Values range by Payment Type')



