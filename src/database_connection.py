
import mysql.connector

def create_connection():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="smart_tourism_db"
        )

        if connection.is_connected():
            print("MySQL Database Connected Successfully!")

        return connection

    except mysql.connector.Error as error:
        print("Database connection failed:", error)
        return None


if __name__ == "__main__":
    connection = create_connection()

    if connection:
        connection.close()
        print("Database connection closed.")
