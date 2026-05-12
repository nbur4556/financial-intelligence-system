import unittest
import sqlite3
import os
import pandas as pd
from scripts.etl import clean_merchant_name

class TestETL(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_finance.db"
        self.schema_path = "schema.sql"
        
        # Initialize test database
        with open(self.schema_path, 'r') as f:
            sql = f.read()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executescript(sql)
        conn.commit()
        conn.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_clean_merchant_name(self):
        """Verify that bank descriptions are cleaned correctly."""
        test_cases = [
            ("Withdrawal Debit STARBUCKS STORE 08477 FRANKLIN TN Date 05/10/26 36 5814 Card 4713", "STARBUCKS STORE 08477"),
            ("Withdrawal POS # UBER * EATS PENDING 1515 3rd Street San Francisco CA Card 7453", "EATS PENDING 1515 3rd Street"),
            ("Deposit Debit Ca Uber XFER Uber Uber CA Date 05/10/26 1 687 5 7299 Card 4713", "Uber XFER Uber Uber"),
            (None, "Unknown"),
            ("", "Unknown")
        ]
        
        for raw, expected in test_cases:
            with self.subTest(raw=raw):
                self.assertEqual(clean_merchant_name(raw), expected)

    def test_duplicate_prevention(self):
        """
        Verify that inserting the same transaction ID twice 
        does not result in duplicate rows.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tx_data = (
            "TXN123", 
            "5/11/2026", 
            "STARBUCKS", 
            -6.86, 
            "Withdrawal Debit STARBUCKS", 
            "test_file.csv"
        )
        
        # First insert
        cursor.execute(
            "INSERT OR IGNORE INTO transactions (transaction_id, date, merchant_name, amount, description, source_file) VALUES (?, ?, ?, ?, ?, ?)",
            tx_data
        )
        
        # Second insert (duplicate)
        cursor.execute(
            "INSERT OR IGNORE INTO transactions (transaction_id, date, merchant_name, amount, description, source_file) VALUES (?, ?, ?, ?, ?, ?)",
            tx_data
        )
        
        conn.commit()
        
        # Verify only one record exists
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE transaction_id = 'TXN123'")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 1, "Duplicate transaction IDs should not be inserted.")

if __name__ == "__main__":
    unittest.main()
