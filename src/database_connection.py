import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_connection(use_db=True):
    """
    Establish a connection to the MySQL database.
    If use_db is False, connects without specifying the database (useful for initial creation).
    """
    try:
        connection_params = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", "")
        }
        
        if use_db:
            connection_params["database"] = "international_debt_db"
            
        connection = mysql.connector.connect(**connection_params)
        
        if connection.is_connected():
            return connection
            
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def close_connection(connection):
    """Closes the database connection."""
    if connection and connection.is_connected():
        connection.close()
        
if __name__ == "__main__":
    # Test connection
    conn = get_database_connection(use_db=False)
    if conn:
        print("Successfully connected to the database server.")
        close_connection(conn)
