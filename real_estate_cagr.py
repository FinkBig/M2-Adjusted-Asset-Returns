import pandas as pd
import numpy as np
from datetime import datetime
import traceback
import os

def calculate_cagr(data, start_year=2008):
    data = data[data.index.year >= start_year]
    if data.empty:
        return None
    start_date, end_date = data.index[0], data.index[-1]
    start_value, end_value = data.iloc[0], data.iloc[-1]
    
    # Debugging: Print start and end values
    print(f"Start Date: {start_date}, Start Value: {start_value}")
    print(f"End Date: {end_date}, End Value: {end_value}")
    
    years = (end_date - start_date).days / 365.25
    cagr = (end_value / start_value) ** (1 / years) - 1
    return cagr

def process_file(file_path, date_column='DATE', value_column='ASPUS'):  # Updated column names
    try:
        df = pd.read_csv(file_path)  # Changed to read_csv for CSV file
        print("File loaded successfully.")  # Debugging line
        df[date_column] = pd.to_datetime(df[date_column].astype(str))  # Adjusted to only use DATE
        df.set_index(date_column, inplace=True)
        df[value_column] = pd.to_numeric(df[value_column], errors='coerce')
        return df[value_column].sort_index().dropna()
    except Exception as e:
        print(f"Error processing file: {e}")  # Print the error message
        return None

file_path = '/Users/cornelius.fink/Documents/Greenfield/Sources/Inflation_adjusted_asset_prices/ASPUS.csv'  # Updated file path
data = process_file(file_path)

if data is not None:
    cagr = calculate_cagr(data, start_year=2015)
    if cagr is not None:
        print(f"Real Estate CAGR since 2015: {cagr:.2%}")  # Updated print statement
    else:
        print("Real Estate: No data available for CAGR calculation since 2015")  # Updated print statement
else:
    print("Real Estate: Failed to process file")  # Updated print statement
