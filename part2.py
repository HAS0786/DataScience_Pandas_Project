import pandas as pd

df = pd.read_csv("online_retail_clean.csv",parse_dates=["InvoiceDate"])

print(df.shape)


print("Two Types of Best-Sellers Products:(by Most selling Units or by most Revenue generated)")


print("Best Seller by Quantity (top 10)")

top_10_by_quantity = df.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(10)

print(top_10_by_quantity)

print("Best Seller by Revenue (top 10)")

top_10_by_revenue = df.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(10)

print(top_10_by_revenue)


print("Now Check at what Time more Products sales")

print("We make 4 new Columns (Year,Month,DayName, Hour) from InvoiceDate")

df["Year"] = df['InvoiceDate'].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["DayName"] = df["InvoiceDate"].dt.day_name()
df["Hour"] = df["InvoiceDate"].dt.hour

print("New Time Features are added")
print(df[["InvoiceDate","Year","Month","DayName","Hour"]].head())

print("\n — —  Sales Trends by Month (Seasonality) — -")

monthly_revenue = df.groupby("Month")["Revenue"].sum().sort_values(ascending=False)
print(monthly_revenue)


daily_revenue = df.groupby("DayName")["Revenue"].sum().sort_values(ascending=False)
print("\n — — Revenue by Day of Week — -")
print(daily_revenue)


hourly_revenue = df.groupby("Hour")["Revenue"].sum().sort_index()
print("\n — — Revenue by Hour of Day — -")
print(hourly_revenue)


df.to_csv("online_retail_best_seller_analyze.csv")