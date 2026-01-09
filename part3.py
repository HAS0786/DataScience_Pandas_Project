import pandas as pd
import numpy as np
from datetime import datetime, timedelta


df = pd.read_csv("online_retail_best_seller_analyze.csv",parse_dates=["InvoiceDate"])

print("Successfully Load Data")
print(df.shape)


print("Calculating RFM (Recency , Frequency , Monetary)")

print("Take a SnapShot")

snapshot_date = df["InvoiceDate"].max() + timedelta(days=1)


rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
    "InvoiceNo":"nunique",
    "Revenue":"sum"
})


rfm.rename(columns={
    "InvoiceDate":"Recency",
    "InvoiceNo":"Frequency",
    "Revenue": "Monetary",
},inplace=True)


# Recency means, When was the last time this customer bought from us?
# Recency = 2
# Translation: “This customer bought something just two days ago.”

# Frequency => “Is this a one-time buyer or someone who keeps coming back?”
# Frequency = 7
# They didn’t just buy once — they came back again and again.

# Monetary=> “Who actually brings in the money?”
# Customer 12346:
# Monetary = £77,183.60
# Frequency = 1
# Recency = 326
# This tells a very specific story:
# A single, very large order… a long time ago… and nothing since.
# Now compare that to Customer 12347:
# Lower total spend
# Multiple purchases
# Very recent activity
print(rfm.head())

def rfm_score(series,ascending=True,n_bins=5):
    ranked = series.rank(method="first",ascending=ascending)
    return pd.qcut(
        ranked,
        q=n_bins,
        labels=range(1,n_bins+1),
    ).astype(int)


rfm["R_Score"] = rfm_score(rfm["Recency"],ascending=False)
rfm["F_Score"] = rfm_score(rfm["Frequency"])
rfm["M_Score"] = rfm_score(rfm["Monetary"])

rfm["RFM_Score"]=(
    rfm["R_Score"].astype(str)
      + rfm["F_Score"].astype(str)
      +rfm["M_Score"].astype(str)
)


def rfm_segment(row):
    if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
        return 'Champions'
    elif row['F_Score'] >= 4:
        return 'Loyal Customers'
    elif row['M_Score'] >= 4:
        return 'Big Spenders'
    elif row['R_Score'] <= 2:
        return 'At-Risk'
    else:
        return 'Others'
rfm['Segment'] = rfm.apply(rfm_segment, axis=1)

print(rfm.head())