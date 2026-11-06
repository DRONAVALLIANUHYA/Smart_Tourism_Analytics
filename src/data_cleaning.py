
import pandas as pd

# Load datasets
passengers = pd.read_csv("data/passenger_data.csv")
bookings = pd.read_csv("data/hotel_bookings.csv")
sales = pd.read_csv("data/sales_data.csv")


# Clean passenger data
passengers["travel_date"] = pd.to_datetime(
    passengers["travel_date"]
)

passengers["travel_time"] = pd.to_datetime(
    passengers["travel_time"],
    format="%H:%M:%S"
).dt.time


# Clean hotel booking data
bookings["check_in"] = pd.to_datetime(
    bookings["check_in"]
)

bookings["check_out"] = pd.to_datetime(
    bookings["check_out"]
)

bookings["booking_duration"] = (
    bookings["check_out"] - bookings["check_in"]
).dt.days


# Clean sales data
sales["sale_date"] = pd.to_datetime(
    sales["sale_date"]
)

sales["total_amount"] = (
    sales["quantity"] * sales["unit_price"]
)


# Save cleaned datasets
passengers.to_csv(
    "data/passenger_data.csv", index=False
)

bookings.to_csv(
    "data/hotel_bookings.csv", index=False
)

sales.to_csv(
    "data/sales_data.csv", index=False
)


print("All datasets cleaned successfully!")

print("\nPassenger date type:")
print(passengers["travel_date"].dtype)

print("\nHotel check-in type:")
print(bookings["check_in"].dtype)

print("\nSales date type:")
print(sales["sale_date"].dtype)

print("\nHotel booking duration added successfully!")
