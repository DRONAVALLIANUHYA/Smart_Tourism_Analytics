
import pandas as pd

# Load datasets
passengers = pd.read_csv("data/passenger_data.csv")
bookings = pd.read_csv("data/hotel_bookings.csv")
sales = pd.read_csv("data/sales_data.csv")

# Inspect passenger data
print("\n========== PASSENGER DATA ==========")
print(passengers.head())
print("\nShape:", passengers.shape)
print("\nColumns:", passengers.columns.tolist())
print("\nMissing Values:")
print(passengers.isnull().sum())

# Inspect hotel booking data
print("\n========== HOTEL BOOKING DATA ==========")
print(bookings.head())
print("\nShape:", bookings.shape)
print("\nMissing Values:")
print(bookings.isnull().sum())

# Inspect sales data
print("\n========== SALES DATA ==========")
print(sales.head())
print("\nShape:", sales.shape)
print("\nMissing Values:")
print(sales.isnull().sum())

print("\nAll datasets inspected successfully!")
