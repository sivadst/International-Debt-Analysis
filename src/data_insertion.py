import pandas as pd
import os
import time
from database_connection import get_database_connection, close_connection

def create_database_and_schema():
    print("Setting up the database and schema...")
    
    # Connect without specifying database to create it
    conn = get_database_connection(use_db=False)
    if not conn:
        print("Could not connect to MySQL server. Check credentials in .env file.")
        return False
        
    cursor = conn.cursor()
    
    # Read schema file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(script_dir, "../sql/schema.sql")
    
    try:
        with open(schema_path, 'r') as f:
            sql_script = f.read()
            
        # Execute schema script statements
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
                
        conn.commit()
        print("Database and tables created successfully.")
        return True
    except Exception as e:
        print(f"Error creating schema: {e}")
        return False
    finally:
        cursor.close()
        close_connection(conn)

def insert_data(cleaned_data_path):
    print(f"Loading cleaned data from {cleaned_data_path}...")
    try:
        df = pd.read_csv(cleaned_data_path)
    except FileNotFoundError:
        print(f"Error: Could not find {cleaned_data_path}. Run data_cleaning.py first.")
        return
        
    conn = get_database_connection(use_db=True)
    if not conn:
        return
        
    cursor = conn.cursor()
    
    try:
        print("Inserting distinct Countries...")
        # Get distinct countries
        countries = df[['country_code', 'country_name']].drop_duplicates()
        
        # Insert countries
        country_insert_query = "INSERT IGNORE INTO Countries (Country_Code, Country_Name) VALUES (%s, %s)"
        cursor.executemany(country_insert_query, countries.values.tolist())
        conn.commit()
        
        print("Inserting distinct Indicators...")
        # Get distinct indicators
        indicators = df[['indicator_code', 'indicator_name']].drop_duplicates()
        
        # Insert indicators
        indicator_insert_query = "INSERT IGNORE INTO Indicators (Indicator_Code, Indicator_Name) VALUES (%s, %s)"
        cursor.executemany(indicator_insert_query, indicators.values.tolist())
        conn.commit()
        
        # To insert Debt_Data, we need the mapping of Country_Code -> Country_ID and Indicator_Code -> Indicator_ID
        print("Fetching lookup tables for IDs...")
        cursor.execute("SELECT Country_Code, Country_ID FROM Countries")
        country_lookup = {row[0]: row[1] for row in cursor.fetchall()}
        
        cursor.execute("SELECT Indicator_Code, Indicator_ID FROM Indicators")
        indicator_lookup = {row[0]: row[1] for row in cursor.fetchall()}
        
        print("Preparing Debt_Data records...")
        # Map IDs back to the dataframe
        df['Country_ID'] = df['country_code'].map(country_lookup)
        df['Indicator_ID'] = df['indicator_code'].map(indicator_lookup)
        
        # Prepare records for insertion
        debt_records = df[['Country_ID', 'Indicator_ID', 'year', 'debt_value']].values.tolist()
        
        print(f"Inserting {len(debt_records)} Debt_Data records... (This may take a moment)")
        debt_insert_query = "INSERT INTO Debt_Data (Country_ID, Indicator_ID, Year, Debt_Value) VALUES (%s, %s, %s, %s)"
        
        # Batch insert for performance
        batch_size = 5000
        for i in range(0, len(debt_records), batch_size):
            batch = debt_records[i:i + batch_size]
            cursor.executemany(debt_insert_query, batch)
            conn.commit()
            
        print("All data inserted successfully!")
        
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        close_connection(conn)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned_data_abs = os.path.join(script_dir, "../data/cleaned/cleaned_debt_data.csv")
    
    if create_database_and_schema():
        insert_data(cleaned_data_abs)
