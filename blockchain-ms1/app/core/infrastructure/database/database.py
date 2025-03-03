import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    """
    Handles the PostgreSQL database connection using psycopg2.
    Ensures a persistent connection for query execution.
    """

    def __init__(self):
        self.connection = None

    def connect(self):
        """Establishes a connection to the PostgreSQL database."""
        if self.connection is None or self.connection.closed:
            try:
                self.connection = psycopg2.connect(os.getenv("POSTGRES_URL"))
                self.connection.autocommit = True
                print("✅ Connected to PostgreSQL")
            except Exception as e:
                print(f"❌ Database connection failed: {e}")
                self.connection = None

    def get_cursor(self):
        """Returns a new cursor for executing queries."""
        if self.connection is None:
            self.connect()
        return self.connection.cursor()

    def close(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")

database = Database()
database.connect()