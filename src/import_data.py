
import pandas as pd
from database_connection import create_connection

# Connect to MySQL
connection = create_connection()

if connection is None:
    exit()

cursor = connection.cursor()

# Load CSV files
passengers = pd.read_csv("data/passenger_data.csv")
bookings = pd.read_csv("data/hotel_bookings.csv")
sales = pd.read_csv("data/sales_data.csv")

# Convert passenger records
passenger_query = """
INSERT INTO passengers
(passenger_id, route, travel_date, travel_time, ticket_price)
VALUES (%s, %s, %s, %s, %s)
"""

passenger_data = [
    (
        row.passenger_id,
        row.route,
        row.travel_date,
        row.travel_time,
        row.ticket_price
    )
    for row in passengers.itertuples(index=False)
]

cursor.executemany(passenger_query, passenger_data)


# Convert hotel booking records
booking_query = """
INSERT INTO hotel_bookings
(booking_id, hotel_name, customer_name, check_in,
 check_out, room_price, booking_status, booking_duration)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

booking_data = [
    (
        row.booking_id,
        row.hotel_name,
        row.customer_name,
        row.check_in,
        row.check_out,
        row.room_price,
        row.booking_status,
        row.booking_duration
    )
    for row in bookings.itertuples(index=False)
]

cursor.executemany(booking_query, booking_data)


# Convert sales records
sales_query = """
INSERT INTO sales
(transaction_id, sale_date, product, quantity,
 unit_price, total_amount)
VALUES (%s, %s, %s, %s, %s, %s)
"""

sales_data = [
    (
        row.transaction_id,
        row.sale_date,
        row.product,
        row.quantity,
        row.unit_price,
        row.total_amount
    )
    for row in sales.itertuples(index=False)
]

cursor.executemany(sales_query, sales_data)

# Save changes
connection.commit()

print("Data imported successfully!")
print("Passenger records:", len(passenger_data))
print("Hotel booking records:", len(booking_data))
print("Sales records:", len(sales_data))

cursor.close()
connection.close()
