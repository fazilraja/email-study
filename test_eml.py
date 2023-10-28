from database import *
import unittest
import sqlite3
import os

eml = "2023-10-05/test1.eml"

class TestEmailFunctions(unittest.TestCase):

    def setUp(self):
        # Initialize a temporary test database
        self.conn = sqlite3.connect(":memory:")  # Use an in-memory database for testing
        self.cursor = self.conn.cursor()
        self.create_database_table()

    def tearDown(self):
        # Close the database connection
        self.conn.close()

    def create_database_table(self):
        # Create the same table as in your main code
        self.cursor.execute('''
            CREATE TABLE emails (
                email_address TEXT PRIMARY KEY,
                to_address TEXT,
                from_address TEXT,
                ip_address TEXT,
                domain_name TEXT,
                email_body TEXT,
                spf_result TEXT
                dkim_result TEXT
            )
        ''')
        self.conn.commit()

    def test_extract_email_details(self):
        # Write test cases for extract_email_details function
        # You can use temporary EML files or mock data
        # Use self.assertEqual or self.assertTrue to check the expected output
        from_address, to_address, subject, _ = extract_email_details(eml)
        #print(f"from_address: {from_address}")
       # print(f"to_address: {to_address}")
        #print(f"subject: {subject}")



    def test_extract_spf_result(self):
        # Write test cases for extract_spf_result function
        # You can use temporary EML files or mock data
        # Use self.assertEqual or self.assertTrue to check the expected output
        spf_result = extract_spf_result(eml)

    def test_database_operations(self):
        # Write test cases for database operations
        # You can use the database connection created in setUp
        # Insert data into the database and then retrieve it to check if it matches
        # Use self.assertEqual or self.assertTrue to check the expected output
        pass

if __name__ == '__main__':
    unittest.main()
