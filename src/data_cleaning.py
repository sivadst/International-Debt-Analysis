import pandas as pd
import numpy as np
import os

def clean_data(input_path, output_path):
    print(f"Loading raw data from {input_path}...")
    
    # 1. Load the dataset into Pandas DataFrame
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}. Please generate or provide the raw dataset first.")
        return

    # Display dataset structure
    print("\n--- Dataset Structure ---")
    print(df.info())
    print(f"\nShape: {df.shape}")
    
    # 2. Filter relevant columns & Standardize
    # Assuming columns: 'Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', '2010', '2011'...
    print("\n--- Standardizing Column Names ---")
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
    
    # Check what year columns exist
    year_columns = [col for col in df.columns if col.isdigit()]
    id_vars = [col for col in df.columns if not col.isdigit()]
    
    print("\n--- Melting Dataset into Long Format ---")
    # Melt the dataset from wide format to long format (Country, Indicator, Year, Debt_Value)
    df_long = pd.melt(df, id_vars=id_vars, value_vars=year_columns, var_name='year', value_name='debt_value')
    
    # 3. Handle missing values
    print("\n--- Handling Missing Values ---")
    missing_before = df_long.isnull().sum().sum()
    # We will drop rows where debt_value is null because an empty debt indicator for a year is non-informative
    df_long = df_long.dropna(subset=['debt_value'])
    missing_after = df_long.isnull().sum().sum()
    print(f"Removed {missing_before - missing_after} missing values.")

    # 4. Remove duplicate records
    print("\n--- Removing Duplicates ---")
    duplicates_before = df_long.duplicated().sum()
    df_long = df_long.drop_duplicates()
    print(f"Removed {duplicates_before} duplicate records.")

    # 5. Perform datatype conversion
    print("\n--- Datatype Conversion ---")
    df_long['year'] = pd.to_numeric(df_long['year'], errors='coerce').astype(int)
    df_long['debt_value'] = pd.to_numeric(df_long['debt_value'], errors='coerce')
    
    # Final check
    print("\n--- Cleaned Dataset Structure ---")
    print(df_long.info())
    print(f"\nShape: {df_long.shape}")
    
    # Save to cleaned data folder
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_long.to_csv(output_path, index=False)
    print(f"\nCleaned data saved successfully to {output_path}")

if __name__ == "__main__":
    raw_data_path = "../data/raw/international_debt.csv"
    cleaned_data_path = "../data/cleaned/cleaned_debt_data.csv"
    
    # Determine absolute paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_abs = os.path.join(script_dir, raw_data_path)
    cleaned_data_abs = os.path.join(script_dir, cleaned_data_path)
    
    clean_data(raw_data_abs, cleaned_data_abs)
