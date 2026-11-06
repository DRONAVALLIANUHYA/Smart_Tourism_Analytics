
from src.database_connection import create_connection
import pandas as pd


def get_data(query):
    connection = create_connection()

    if connection is None:
        return pd.DataFrame()

    try:
        df = pd.read_sql(query, connection)
        return df

    except Exception as error:
        print("Query error:", error)
        return pd.DataFrame()

    finally:
        connection.close()


# 1. Passenger Analytics
def passenger_analytics():

    query = """
    SELECT
        route,
        COUNT(*) AS total_passengers,
        SUM(ticket_price) AS total_revenue
    FROM passengers
    GROUP BY route
    ORDER BY total_passengers DESC
    """

    return get_data(query)


# 2. Hotel Analytics
def hotel_analytics():

    query = """
    SELECT
        hotel_name,
        COUNT(*) AS total_bookings,
        SUM(
            CASE
                WHEN booking_status = 'Cancelled' THEN 1
                ELSE 0
            END
        ) AS cancelled_bookings
    FROM hotel_bookings
    GROUP BY hotel_name
    ORDER BY total_bookings DESC
    """

    return get_data(query)


# 3. Sales Analytics
def sales_analytics():

    query = """
    SELECT
        product,
        SUM(quantity) AS total_quantity,
        SUM(total_amount) AS total_revenue
    FROM sales
    GROUP BY product
    ORDER BY total_revenue DESC
    """

    return get_data(query)


# Test all analytics
if __name__ == "__main__":

    print("\nPASSENGER ANALYTICS")
    print(passenger_analytics())

    print("\nHOTEL ANALYTICS")
    print(hotel_analytics())

    print("\nSALES ANALYTICS")
    print(sales_analytics())
