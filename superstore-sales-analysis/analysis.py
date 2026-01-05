# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('SuperstoreSales.csv', encoding='latin1')

# Data exploration
print(df.head())
print("Size of Data:",df.shape)
print(df.columns)
print(df.dtypes)
print("Missing values:\n", df.isnull().sum())
print("Duplicate rows: ", df.duplicated().sum())

# Remove duplicate values
df = df.drop_duplicates()

# Convert to datetime format
df["Order Date"] = pd.to_datetime(
    df["Order Date"], 
    dayfirst=False, 
    errors="coerce"
    )
df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    dayfirst=False,
    errors="coerce")


# Again Data check
print(df.head())
print("Final Size of Data:",df.shape)
print("Missing values:\n", df.isnull().sum())
print("Duplicate rows: ", df.duplicated().sum())
print(df.dtypes)

# Basic Data Analysis
total_sale = np.sum(df["Sales"].to_numpy())
total_profit = np.sum(df["Profit"].to_numpy())
avg_sale = np.mean(df["Sales"].to_numpy())
avg_profit = np.mean(df["Profit"].to_numpy())

print("\nOverall Sales and Profit Analysis:")
print("Total Sales:", total_sale)
print("Total Profit:", total_profit)
print("Average Sales:", avg_sale)
print("Average Profit:", avg_profit)

# Sales and Profit by Category
category_analysis = df.groupby("Category")[["Sales", "Profit"]].sum()
print("\nCategory Sales and Profit Analysis:\n", category_analysis)

# Profit by Region
region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
print("\nProfit by Region:\n", region_profit)

# Top 10 Products by Sales
top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Products by Sales:\n", top_products)

# Monthly Sales Trend
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("Month")["Sales"].sum()

# Visualizations
# # Monthly Sales Trend
plt.figure("Monthly Sales", figsize=(12, 6))
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.xlabel("Months", fontsize=12 ,weight='bold')
plt.ylabel("Total Sales", fontsize=12, weight='bold')
plt.xticks(
    range(0, len(monthly_sales.index), 4), 
    monthly_sales.index[::4], 
    rotation=45
    )
plt.grid()
plt.tight_layout()
plt.show()

# Sales by Category
category_sales = df.groupby("Category")["Sales"].sum()

plt.figure("Category Sales", figsize=(8, 5))
category_sales.plot(kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category", fontsize=12, weight='bold')
plt.ylabel("Total Sales", fontsize=12, weight='bold')
plt.xticks(rotation=0)
plt.show()

# Profit by Region
plt.figure("Region Profit", figsize=(8, 5))
region_profit.plot(kind="bar")
plt.title("Profit by Region")
plt.xlabel("Region", fontsize=12, weight='bold')
plt.ylabel("Total Profit", fontsize=12, weight='bold')
plt.xticks(rotation=0)
plt.show()

# Sales Distribution by Category Pie Chart
plt.figure("Pie Chart - Category Sales")
plt.pie(
    category_sales,
    labels=category_sales.index,
    autopct="%1.1f%%",
    textprops={"fontsize": 10},
    startangle=90
    )
plt.title("Sales Distribution by Category", fontsize=14)
plt.axis("equal")
plt.tight_layout()
plt.show()
