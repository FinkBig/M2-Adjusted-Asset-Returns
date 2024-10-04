import pandas as pd

def process_file(file_path, date_column='Date', value_column='Close/Last'):
    try:
        df = pd.read_csv(file_path)  # Read CSV file
        print("File loaded successfully.")  # Debugging line
        
        # Convert the date column to datetime format
        df[date_column] = pd.to_datetime(df[date_column])
        df.set_index(date_column, inplace=True)
        
        # Convert the value column to numeric, handling errors
        df[value_column] = pd.to_numeric(df[value_column], errors='coerce')
        
        # Return sorted and cleaned data
        return df[value_column].sort_index().dropna()
    except Exception as e:
        print(f"Error processing file: {e}")  # Print the error message
        return None

def calculate_cagr(data, start_year, end_year):
    start_value = data[data.index.year == start_year].iloc[0]  # Get the value at the start year
    end_value = data[data.index.year == end_year].iloc[-1]  # Get the value at the end year
    years = end_year - start_year  # Calculate the number of years
    if start_value > 0:
        return (end_value / start_value) ** (1 / years) - 1  # Calculate CAGR
    return None

# Define the file path and columns for SPXT data
file_path = '/Users/cornelius.fink/Documents/Greenfield/Sources/Inflation_adjusted_asset_prices/spxt_data.csv'
date_column = 'Date'
value_column = 'Close/Last'

# Process the SPXT file
data = process_file(file_path, date_column, value_column)

# Calculate and print the CAGR for SPXT from 2015 to 2024
if data is not None:
    cagr = calculate_cagr(data, start_year=2015, end_year=2024)  # Calculate CAGR from 2015 to 2024
    if cagr is not None:
        print(f"SPXT CAGR from 2015 to 2024: {cagr:.2%}")  # Print the result
    else:
        print("SPXT: No data available for CAGR calculation from 2015 to 2024")  # Handle no data case
else:
    print("SPXT: Failed to process file")  # Handle processing failure
