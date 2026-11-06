
import pandas as pd

# Load datasets
passengers = pd.read_csv("data/passenger_data.csv")
bookings = pd.read_csv("data/hotel_bookings.csv")
sales = pd.read_csv("data/sales_data.csv")

# Function to check data quality
def check_quality(df, name):

    print(f"\n========== {name} ==========")

    # Check duplicate records
    print("Duplicate records:", df.duplicated().sum())

    # Check missing values
    print("Missing values:", df.isnull().sum().sum())

    # Check data types
    print("\nData Types:")
    print(df.dtypes)


# Check all datasets
check_quality(passengers, "PASSENGER DATA")
check_quality(bookings, "HOTEL BOOKING DATA")
check_quality(sales, "SALES DATA")


# Check invalid passenger prices
print("\nInvalid passenger prices:",
      (passengers["ticket_price"] <= 0).sum())

# Check invalid hotel prices
print("Invalid hotel prices:",
      (bookings["room_price"] <= 0).sum())

# Check invalid sales quantities
print("Invalid sales quantities:",
      (sales["quantity"] <= 0).sum())

# Check incorrect hotel dates
check_in = pd.to_datetime(bookings["check_in"])
check_out = pd.to_datetime(bookings["check_out"])

print("Invalid hotel date records:",
      (check_out <= check_in).sum())

print("\nData quality checking completed!")
