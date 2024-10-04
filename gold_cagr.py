import pandas as pd

def process_file(file_path, year_column='YEAR', value_column='PRICE'):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)  # Read CSV file
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl')  # Read Excel file
        else:
            raise ValueError("Unsupported file format")

        print("File loaded successfully.")  # Debugging line
        df[year_column] = pd.to_datetime(df[year_column].astype(str), format='%Y')  # Convert YEAR to datetime
        df.set_index(year_column, inplace=True)
        df[value_column] = pd.to_numeric(df[value_column], errors='coerce')  # Convert PRICE to numeric
        return df[value_column].sort_index().dropna()  # Return sorted and cleaned data
    except Exception as e:
        print(f"Error processing file: {e}")  # Print the error message
        return None

def calculate_cagr(data, start_year):
    start_value = data[data.index.year == start_year].iloc[0]  # Get the value at the start year
    end_value = data.iloc[-1]  # Get the last value
    years = data.index.year[-1] - start_year  # Calculate the number of years
    if start_value > 0:
        return (end_value / start_value) ** (1 / years) - 1  # Calculate CAGR
    return None

# Define the file path and columns for Gold
file_path = '/Users/cornelius.fink/Documents/Greenfield/Sources/Inflation_adjusted_asset_prices/goldprice.xlsx'
year_column = 'YEAR'
value_column = 'PRICE'

# Process the gold file
data = process_file(file_path, year_column, value_column)

# Calculate and print the CAGR for Gold
if data is not None:
    cagr = calculate_cagr(data, start_year=2015)  # Calculate CAGR since 2015
    if cagr is not None:
        print(f"Gold CAGR since 2015: {cagr:.2%}")  # Print the result
    else:
        print("Gold: No data available for CAGR calculation since 2015")  # Handle no data case
else:
    print("Gold: Failed to process file")  # Handle processing failure
