

# --------------- Import Libraries ---------------

import pandas as pd
import matplotlib.pyplot as plt

# ---------------- Load Dataset ----------------

# Load dataset
df = pd.read_csv(r"C:\Datasets\E_Commerce.csv")


# ---------------- Data Cleaning ----------------

# Keep only necessary columns
df = df[['event_time', 'order_id', 'product_id', 'brand', 'price', 'user_id']]

# Convert data types
df['event_time'] = pd.to_datetime(df['event_time'])
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Handle missing values
df['brand'] = df['brand'].fillna('Unknown')

# Drop invalid rows
df = df.dropna(subset=['price', 'user_id'])
df = df[df['price'] > 0]

# Remove duplicates
df = df.drop_duplicates()


# ---------------- Data Overview ----------------
df.info()

print("\nDataset Preview:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())


# ---------------- Revenue Analysis ----------------

# Calculate total revenue generated

total_revenue = df['price'].sum()
print("Total Revenue:", total_revenue)

revenue_brand = df.groupby('brand')['price'].sum().sort_values(ascending=False)

print("\nTop 10 revenue-generating brands:")
print(revenue_brand.head(10))

print("\nInsight: A small number of brands contribute a large portion of total revenue, indicating strong brand concentration.")


top_products = df.groupby('product_id')['price'].sum().sort_values(ascending=False)
print("\nTop 10 products by revenue:")
print(top_products.head(10))

print("\nInsight: High-performing products drive significant revenue, suggesting focus areas for inventory and marketing.")


# ---------------- Customer Behavior Analysis ----------------

print("Total Users:", df['user_id'].nunique())

orders_per_user = df.groupby('user_id')['order_id'].nunique()

print("\nOrder distribution per user:")
print(orders_per_user.describe())

print("\nInsight: Most users place very few orders, indicating a large base of low-engagement customers.")

# Top users

top_users = df.groupby('user_id')['price'].sum().sort_values(ascending=False).head(10)
print("\nTop 10 users by spending:")
print(top_users)

print("\nInsight: A small group of high-value customers contributes disproportionately to revenue.")


# ---------------- Time-Based Trend Analysis ----------------

df['date'] = df['event_time'].dt.date
df['hour'] = df['event_time'].dt.hour

orders_day = df.groupby('date')['order_id'].count()
revenue_day = df.groupby('date')['price'].sum()

orders_hour = df.groupby('hour')['order_id'].count()
print("\nPeak order hours:")
print(orders_hour.sort_values(ascending=False).head(3))

print("\nInsight: Orders peak during specific hours, useful for targeted promotions and staffing decisions.")


# ---------------- Customer-Level Aggregation ----------------

# Order Frequency per User

user_orders = df.groupby('user_id')['order_id'].nunique().sort_values(ascending=False)
print("\nTop users by order frequency:")
print(user_orders.head(10))

# Average spending per user

avg_spend_user = df.groupby('user_id')['price'].mean().sort_values(ascending=False).head(10)
print("\nTop users by average spend:")
print(avg_spend_user)

print("\nInsight: These users spend more per transaction, indicating premium buying behavior.")


# ---------------- Visualization ----------------

plt.figure(figsize=(10,5))
revenue_brand.head(10).plot(kind='bar')
plt.title("Top Brands by Revenue")
print("\nInsight: Top brands dominate revenue contribution, suggesting dependency on a few key brands.")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10,5))
orders_hour.plot(kind='line')
plt.title("Orders by Hour")
print("\nInsight: Orders peak during specific hours, showing clear high-activity periods for targeted marketing.")
plt.show()

plt.figure(figsize=(10,5))
revenue_day.plot()
plt.title("Revenue Trend Over Time")
print("\nInsight: Revenue fluctuates over time, indicating changing customer demand and possible seasonal patterns.")
plt.show()

top_users.plot(kind='bar')
plt.title("Top 10 Users by Spending")
print("\nInsight: A small group of users contributes a large share of revenue, highlighting high-value customers.")
plt.xlabel("User ID")
plt.ylabel("Total Spend")
plt.show()

orders_per_user.plot(kind='hist', bins=30)
plt.title("Distribution of Orders per User")
print("\nInsight: Most users place very few orders, indicating low engagement and retention challenges.")
plt.xlabel("Number of Orders")
plt.ylabel("Frequency")
plt.show()

avg_spend_user.plot(kind='bar')
plt.title("Top Users by Average Spend")
print("\nInsight: Some users have high average spending, representing premium customers with strong revenue impact.")
plt.show()


# ---------------- Summary Statistics ----------------

print("\nSummary statistics:")
print(df.describe())

print("\nInsight: The data shows variation in pricing, indicating presence of both low and high-value transactions.")




