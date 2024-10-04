import pandas as pd

def calculate_cagr(data, start_year=2015):
    data = data[data.index.year >= start_year]
    if data.empty:
        return None
    start_date, end_date = data.index[0], data.index[-1]
    start_value, end_value = data.iloc[0], data.iloc[-1]
    years = (end_date - start_date).days / 365.25
    cagr = (end_value / start_value) ** (1 / years) - 1
    return cagr

def process_crypto_file(file_path, date_column='DATE', value_column='MCAP'):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
        df[date_column] = pd.to_datetime(df[date_column], unit='ms')  # Convert milliseconds to datetime
        df[value_column] = pd.to_numeric(df[value_column], errors='coerce')  # Ensure MCAP is numeric
        df.set_index(date_column, inplace=True)
        return df[value_column].sort_index().dropna()
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

# File path to the total crypto market cap data
file_path = '/Users/cornelius.fink/Documents/Greenfield/Sources/Inflation_adjusted_asset_prices/totalcryptomcap.csv'

# Process the file and calculate CAGR
data = process_crypto_file(file_path)
if data is not None:
    cagr = calculate_cagr(data, start_year=2015)
    if cagr is not None:
        print(f"Total Crypto Market Cap CAGR since 2015: {cagr:.2%}")
    else:
        print("No data available for CAGR calculation since 2015")
else:
    print("Failed to process the crypto market cap file.")