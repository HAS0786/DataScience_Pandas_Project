import pandas as pd
import numpy as np

File_Path = "Online Retail.csv"
Sample_fraction = 0.1
df = pd.read_csv(File_Path,encoding="unicode_escape")
print(df.shape)


# Take 10% random data:
dff = df.sample(frac=Sample_fraction,random_state=42).reset_index(drop=True)

# print(df.head(142))
print(dff.head())
print(dff.tail())
print(dff.info())
print(dff.describe())
print(dff.shape)  #before any thing



print("Description (Null entities Deleted )")

dff.dropna(subset=["Description"],inplace=True)

print(dff["Description"].isnull().sum())


print("InvoiceDate (change from Object to DateTime)")

dff["InvoiceDate"] = pd.to_datetime(dff["InvoiceDate"])
print(dff["InvoiceDate"].dtype)


print("Remove Duplicated Rows")

num_duplicated = dff.duplicated().sum()

print(f"Found {num_duplicated} fully duplicated rows")

dff.drop_duplicates(inplace=True)

print(f"Data Frames after removing Duplicates: {len(dff)} rows")
print(dff.shape)


print("Remove those whose Quantity value is not less than 0, that provide us the Sales not returns")

dff = dff[dff["Quantity"]>0]

print("Remove those whose Unitprice is 0(free) or some error")

dff = dff[dff["UnitPrice"]>0]

print(f"DataFrames after Filtering: {len(dff)} rows")
print(dff.shape)

print("Cleaning the Description from Leading and Trailing Spaces")

dff["Description"] = dff["Description"].str.strip()

print("Cleaning the Countries from Leading and Trailing Spaces")

dff["Country"] = dff["Country"].str.strip()

print("Handling Name inconsistencies like (EIRE for Ireland)")
dff["Country"].replace("EIRE","Ireland",inplace=True)

print("Now Text Columns are Cleaned and Standardized (no duplication , no inconsistencies or no extra spaces)")

print("Add a new Columns of Revenue for checking sales as now only we have UnitPrice and Quantity saled")

dff["Revenue"] = dff["Quantity"]*dff["UnitPrice"]

print("Top Revenue Countries")

top_countries = dff.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10)

print("\n\n ---- Top 10 Countries by Revenue ----")
print(top_countries)

print(dff.shape)
dff.to_csv("online_retail_clean.csv")
