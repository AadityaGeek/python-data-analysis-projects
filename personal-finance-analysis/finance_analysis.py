# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("finance_summary.csv")

# Initial data exploration
print("\nInitial Data Exploration:\n")
print(df.info())
print(df.shape)
print(df.columns)
print("\nMissing values:\n", df.isnull().sum())
print("\nDuplicate rows: ", df.duplicated().sum())

# Drop unnecessary columns
df = df.drop(columns=['transfer-currency',
                      'to-account',
                      'receive-amount',
                      'receive-currency',
                      'description',
                      'due-date',
                      'id'
                      ]
            )


# Data cleaning and type conversion
df["Date"] = pd.to_datetime(df["Date"])
df["amount"] = df["amount"].str.replace(",","")
df["amount"] = pd.to_numeric(df["amount"])
df["transfer-amount"] = df["transfer-amount"].str.replace(",","")
df["transfer-amount"] = pd.to_numeric(df['transfer-amount'])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month

# Handle missing values
df["title"] = df["title"].fillna("Unknown")
df["category"] = df["category"].fillna("Other")

# Post-cleaning exploration
print("\nPost-cleaning Data Exploration:\n")
print(df.dtypes)
print(df.head())
print("\nMissing values:\n", df.isnull().sum())
print("\nDuplicate rows: ", df.duplicated().sum())

# Analysis by transaction type
diff_types = df.groupby('type')[['amount','transfer-amount']].sum()
print("\nTransaction Types Summary:\n")
print(diff_types)

# Separate dataframes for each transaction type
expense_df = df[df['type'] == 'EXPENSE']
income_df = df[df['type'] == 'INCOME']
transfer_df = df[df['type'] == 'TRANSFER']

print(expense_df.shape)
print(income_df.shape)
print(transfer_df.shape)

# Calculate total income, expense, and net savings
total_income = np.sum(income_df['amount'].to_numpy())
total_expense = np.sum(expense_df['amount'].to_numpy())
net_savings = total_income - total_expense
print("\nTotal Income: ", total_income)
print("Total Expense: ", total_expense)
print("Net Savings: ", net_savings)

# Monthly analysis
monthly_income = (
    income_df.groupby(['Year','Month'])['amount'].sum().reset_index()
)
monthly_expense = (
    expense_df.groupby(['Year','Month'])['amount'].sum().reset_index()
)
print("\nMonthly Income:\n")
print(monthly_income)
print("\nMonthly Expense:\n")
print(monthly_expense)

# Merge monthly income and expense dataframes
monthly_summary = pd.merge(
    monthly_income,
    monthly_expense,
    on=['Year', 'Month'],
    how='outer',
    suffixes=('_income', '_expense')
)
monthly_summary = monthly_summary.fillna(0) # Fill NaN values with 0

monthly_summary["savings"] = monthly_summary["amount_income"] - monthly_summary["amount_expense"]

# Add a month_year column for better x-axis representation
monthly_summary["Month_Year"] = (
    monthly_summary["Year"].astype(str) + "-" +
    monthly_summary["Month"].astype(str).str.zfill(2)
    )
print("\nMonthly Summary:\n")
print(monthly_summary)


# Visualizations
# Plot monthly income and expense
plt.figure("Income Expense Graph", figsize=(10, 5))
plt.plot(
    monthly_summary["Month_Year"],
    monthly_summary["amount_income"],
    marker='o',
    label='Income'
)
plt.plot(
    monthly_summary["Month_Year"],
    monthly_summary["amount_expense"],
    marker='o',
    label='Expense'
)
plt.xlabel('Months', weight='bold')
plt.ylabel('Amount', weight='bold')
plt.title('Monthly Income vs Expense')
plt.grid(axis='y')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Category-wise expense analysis
category_expense = expense_df.groupby('category')['amount'].sum().sort_values(ascending=False)
print("\nCategory-wise Expense:\n")
print(category_expense)

plt.figure("Category-wise Expense", figsize=(6, 6))
plt.pie(
    category_expense.values,
    labels=category_expense.index,
    autopct='%1.1f%%'
)
plt.title("Expense Distribution by Category")
plt.show()


# Account-wise expense analysis
account_expense = expense_df.groupby('account')['amount'].sum()
print("\nAccount-wise Expense:\n")
print(account_expense)

plt.figure("Account-wise Expense",figsize=(8, 5))
plt.bar(
    account_expense.index,
    account_expense.values
)
plt.title("Account wise Expense")
plt.xlabel("Account", weight='bold')
plt.ylabel("Expense Amount", weight='bold')
plt.gca().set_axisbelow(True)
plt.grid(axis='y')
plt.show()