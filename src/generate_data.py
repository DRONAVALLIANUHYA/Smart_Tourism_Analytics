
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()
random.seed(42)
Faker.seed(42)

# Create data folder
os.makedirs("data", exist_ok=True)

# 1. PASSENGER DATA
passengers = []

routes = [
    "Fujiyoshida - Kawaguchiko",
    "Kawaguchiko - Otsuki",
    "Fujiyoshida - Mount Fuji"
]

for i in range(1, 1001):
    passengers.append({
        "passenger_id": i,
        "route": random.choice(routes),
        "travel_date": fake.date_between(
            start_date="-1y", end_date="today"
        ),
        "travel_time": fake.time(),
        "ticket_price": random.choice([500, 800, 1000, 1200, 1500])
    })

passenger_df = pd.DataFrame(passengers)
passenger_df.to_csv("data/passenger_data.csv", index=False)


# 2. HOTEL BOOKING DATA
bookings = []

hotels = [
    "Fuji View Hotel",
    "Lake Kawaguchi Hotel",
    "Mountain Resort",
    "Tourist Inn"
]

for i in range(1, 501):
    check_in = fake.date_between(
        start_date="-1y", end_date="today"
    )
    check_out = check_in + timedelta(days=random.randint(1, 5))

    bookings.append({
        "booking_id": i,
        "hotel_name": random.choice(hotels),
        "customer_name": fake.name(),
        "check_in": check_in,
        "check_out": check_out,
        "room_price": random.randint(5000, 20000),
        "booking_status": random.choice(
            ["Confirmed", "Cancelled", "Completed"]
        )
    })

booking_df = pd.DataFrame(bookings)
booking_df.to_csv("data/hotel_bookings.csv", index=False)


# 3. SALES DATA
sales = []

products = [
    "Food",
    "Beverages",
    "Souvenirs",
    "Tickets",
    "Travel Accessories"
]

for i in range(1, 1001):
    quantity = random.randint(1, 5)
    unit_price = random.randint(300, 3000)

    sales.append({
        "transaction_id": i,
        "sale_date": fake.date_between(
            start_date="-1y", end_date="today"
        ),
        "product": random.choice(products),
        "quantity": quantity,
        "unit_price": unit_price,
        "total_amount": quantity * unit_price
    })

sales_df = pd.DataFrame(sales)
sales_df.to_csv("data/sales_data.csv", index=False)


print("All datasets generated successfully!")
print("Passenger records:", len(passenger_df))
print("Hotel booking records:", len(booking_df))
print("Sales records:", len(sales_df))
