"""Basic data-quality tests for the Smart Tourism Analytics sample datasets."""

from pathlib import Path
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


class TourismDatasetTests(unittest.TestCase):
    def load_dataset(self, filename):
        path = DATA_DIR / filename
        self.assertTrue(path.exists(), f"Dataset not found: {path}")
        frame = pd.read_csv(path)
        self.assertFalse(frame.empty, f"{filename} should not be empty")
        return frame

    def test_passenger_dataset(self):
        data = self.load_dataset("passenger_data.csv")

        required = {
            "passenger_id", "route", "travel_date",
            "travel_time", "ticket_price"
        }
        self.assertTrue(required.issubset(data.columns))
        self.assertFalse(data["passenger_id"].duplicated().any())
        self.assertTrue(pd.to_datetime(data["travel_date"], errors="coerce").notna().all())
        self.assertTrue(pd.to_numeric(data["ticket_price"], errors="coerce").notna().all())
        self.assertTrue((pd.to_numeric(data["ticket_price"]) >= 0).all())

    def test_hotel_booking_dataset(self):
        data = self.load_dataset("hotel_bookings.csv")

        required = {
            "booking_id", "hotel_name", "customer_name",
            "check_in", "check_out", "room_price", "booking_status"
        }
        self.assertTrue(required.issubset(data.columns))
        self.assertFalse(data["booking_id"].duplicated().any())

        check_in = pd.to_datetime(data["check_in"], errors="coerce")
        check_out = pd.to_datetime(data["check_out"], errors="coerce")
        self.assertTrue(check_in.notna().all())
        self.assertTrue(check_out.notna().all())
        self.assertTrue((check_out >= check_in).all())

        room_prices = pd.to_numeric(data["room_price"], errors="coerce")
        self.assertTrue(room_prices.notna().all())
        self.assertTrue((room_prices >= 0).all())

    def test_sales_dataset(self):
        data = self.load_dataset("sales_data.csv")

        required = {
            "transaction_id", "sale_date", "product",
            "quantity", "unit_price", "total_amount"
        }
        self.assertTrue(required.issubset(data.columns))
        self.assertFalse(data["transaction_id"].duplicated().any())
        self.assertTrue(pd.to_datetime(data["sale_date"], errors="coerce").notna().all())

        quantity = pd.to_numeric(data["quantity"], errors="coerce")
        unit_price = pd.to_numeric(data["unit_price"], errors="coerce")
        total_amount = pd.to_numeric(data["total_amount"], errors="coerce")

        self.assertTrue(quantity.notna().all())
        self.assertTrue(unit_price.notna().all())
        self.assertTrue(total_amount.notna().all())
        self.assertTrue((quantity > 0).all())
        self.assertTrue((unit_price >= 0).all())
        self.assertTrue((total_amount >= 0).all())


if __name__ == "__main__":
    unittest.main(verbosity=2)
