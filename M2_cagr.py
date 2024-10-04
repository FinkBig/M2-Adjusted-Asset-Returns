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
    years = (end_date - start_date).days / 365.25
    cagr = (end_value / start_value) ** (1 / years) - 1
    return cagr

def process_file(file_path, date_column='DATE', value_column='VALUE'):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            return None

        if date_column == 'YEAR':
            df[date_column] = pd.to_datetime(df[date_column].astype(str) + '-01-01')
        else:
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

        df.set_index(date_column, inplace=True)
        df[value_column] = pd.to_numeric(df[value_column], errors='coerce')
        return df[value_column].sort_index().dropna()
    except Exception:
        return None

# Filter to only include the M2 file
files = [
    ('/Users/cornelius.fink/Documents/Greenfield/Sources/Inflation_adjusted_asset_prices/M2SL.csv', 'DATE', 'M2SL')
]

output = []
for file_path, date_column, value_column in files:
    asset_name = file_path.split('/')[-1].split('.')[0]
    data = process_file(file_path, date_column, value_column)
    
    if data is not None:
        cagr = calculate_cagr(data, start_year=2015)  # Change start_year to 2015
        if cagr is not None:
            output.append(f"{asset_name} CAGR since 2015: {cagr:.2%}")  # Updated to include time period
        else:
            output.append(f"{asset_name}: No data available for CAGR calculation since 2015")  # Updated to include time period
    else:
        output.append(f"{asset_name}: Failed to process file")  # Updated to include time period

# Print results to console
print("CAGR Calculation Results:")
for result in output:
    print(result)