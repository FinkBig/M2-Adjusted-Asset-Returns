import pandas as pd
import numpy as np
from datetime import datetime
import traceback
import os

def calculate_cagr(data, start_year, end_year):
    # Print available years in the data
    available_years = data.index.year.unique()
    print(f"Available years in data: {available_years}")

    # Check if the start year exists in the data
    if start_year not in available_years:
        print(f"Start year {start_year} not found in data.")
        return None
    
    # Check if the end year exists in the data
    if end_year not in available_years:
        print(f"End year {end_year} not found in data.")
        return None

    start_value = data[data.index.year == start_year].iloc[0]  # Get the value at the start year
    end_value = data[data.index.year == end_year].iloc[-1]  # Get the value at the end year
    years = end_year - start_year  # Calculate the number of years
    if start_value > 0:
        return (end_value / start_value) ** (1 / years) - 1  # Calculate CAGR
    return None

def process_file(file_path, year_column='YEAR', value_column='PRICE'):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')  # Read Excel file
        print("File loaded successfully.")  # Debugging line
        
        # Convert the year column to datetime format
        df[year_column] = pd.to_datetime(df[year_column].astype(str), format='%Y')
        df.set_index(year_column, inplace=True)
        
        # Convert the value column to numeric, handling errors
        df[value_column] = pd.to_numeric(df[value_column], errors='coerce')
        
        # Return sorted and cleaned data
        return df[value_column].sort_index().dropna()
    except Exception as e:
        print(f"Error processing file: {e}")  # Print the error message
        return None

# Define the file path and columns for SP500 data
file_path = '/Users/cornelius.fink/Documents/Greenfield/Sources/Inflation_adjusted_asset_prices/SP500.xlsx'
year_column = 'YEAR'
value_column = 'PRICE'

# Process the SP500 file
data = process_file(file_path, year_column, value_column)

# Print the data to check its contents
print(data)

# Calculate and print the CAGR for SP500 from 2015 to 2023
if data is not None:
    cagr = calculate_cagr(data, start_year=2015, end_year=2023)  # Calculate CAGR from 2015 to 2023
    if cagr is not None:
        print(f"SP500 CAGR from 2015 to 2023: {cagr:.2%}")  # Print the result
    else:
        print("SP500: No data available for CAGR calculation from 2015 to 2023")  # Handle no data case
else:
    print("SP500: Failed to process file")  # Handle processing failure
