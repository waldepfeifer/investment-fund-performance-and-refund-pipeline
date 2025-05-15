import pandas as pd
import os
import sys

#Fund Composition
fund_df = pd.DataFrame({
    'Company': ['Facebook (Meta)', 'Netflix', 'Apple', 'Tesla', 'Google (Alphabet)', 'Amazon'],
    'Percentage': [0.15, 0.10, 0.25, 0.15, 0.20, 0.15],
    'Symbol': ['META', 'NFLX', 'AAPL', 'TSLA', 'GOOGL', 'AMZN']
})

# csv about users who invested
users_invested = 'users.csv'

# csv with name of output file
users_refund = 'users_refund.csv'

#Load data: Date, Close columns required
def load_market_data(folder_path):
    market_data = pd.concat(
        [pd.read_csv(os.path.join(folder_path, file), usecols=["Date", "Close"])
        .assign(Symbol=file.split('.')[0].split('_')[0])
        for file in os.listdir(folder_path)
        if file.endswith('.csv') and file not in [users_invested, users_refund]]
    )
    # Parse date
    market_data['Date'] = pd.to_datetime(pd.to_datetime(market_data['Date'], utc=True).dt.date)
    market_data = market_data.sort_values(by=['Symbol', 'Date'])
    return market_data


def calculate_stock_performance(df):
    # Add columns for previous period open and close
    df['Last Period Close'] = df.groupby('Symbol')['Close'].shift(1)
    
    # Drop rows with NaN in 'Last Period Close'
    df = df.dropna(subset=['Last Period Close']).reset_index(drop=True)
    
    # Calculate performance metrics
    df['Performance on Close'] = df['Close'] - df['Last Period Close']
    df['Performance on Close %'] = (df['Performance on Close'] / df['Last Period Close']) * 100
    
    # Drop unneeded columns
    df = df.drop(columns=['Close', 'Last Period Close', 'Performance on Close'])
    
    return df

def calculate_fund_performance(fund_df, stock_performance_df):
    # Merge fund and stock performance dataframes
    merged_df = pd.merge(fund_df[['Symbol', 'Percentage']], stock_performance_df, on='Symbol', how='inner')
    
    # Calculate fund performance based on close and open
    merged_df['Fund Performance on Close %'] = merged_df['Performance on Close %'] * merged_df['Percentage']
    
    # Drop unneeded columns
    merged_df = merged_df.drop(columns=['Symbol', 'Percentage', 'Performance on Close %'])
    
    # Aggregate by date
    agg_df = merged_df.groupby('Date').sum().reset_index()
    
    return agg_df

def calculate_cumulative_fund_performance(agg_df):
    # Calculate cumulative performance on open and close
    agg_df['Cumulative Fund Performance on Close %'] = ((1 + agg_df['Fund Performance on Close %'] / 100).cumprod() - 1) * 100
    
    # Drop unneeded columns
    cu_fund_df = agg_df.drop(columns=['Fund Performance on Close %'])
    
    return cu_fund_df

def load_user_data(folder_path):
    # Construct the full path to 'users_invested file'
    file_path = os.path.join(folder_path, users_invested)
    
    # Check if users invested file exists in the folder
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No file named {users_invested} found in the specified folder: {folder_path}")
    
    # Load the CSV file into a DataFrame
    user_data = pd.read_csv(file_path)
    
    # Convert date columns to datetime
    user_data['investment_open_date'] = pd.to_datetime(user_data['investment_open_date'])
    user_data['investment_close_date'] = pd.to_datetime(user_data['investment_close_date'])
    
    return user_data

def calculate_user_refund(users_df, agg_df):
    # Merge to get cumulative fund performance on the investment open date.
    joined_df = pd.merge(users_df, agg_df[['Date', 'Cumulative Fund Performance on Close %']].rename(columns={'Cumulative Fund Performance on Close %': 'Cumulative Fund Performance on Open %'}), 
                         left_on='investment_open_date', right_on='Date', how='left')
    
    # Merge to get cumulative fund performance on the investment close date
    combined_df = pd.merge(joined_df, agg_df[['Date', 'Cumulative Fund Performance on Close %']], 
                           left_on='investment_close_date', right_on='Date', how='left')
    
    # Calculate the refund amount based on performance
    combined_df['amount_refund'] = combined_df['amount_invested'] * (
        1 + combined_df['Cumulative Fund Performance on Close %'] / 100 - combined_df['Cumulative Fund Performance on Open %'] / 100
    )
    
    # Select relevant columns for output
    output_df = combined_df[['user_id', 'investment_open_date', 'investment_close_date', 'amount_invested', 'amount_refund']]
    
    return output_df

def export_to_csv(output_df, folder_path, filename=users_refund):
    # Ensure folder path exists; if not, create it
    os.makedirs(folder_path, exist_ok=True)
    
    # Build the full file path
    file_path = os.path.join(folder_path, filename)
    
    # Export dataframe to CSV with specified formatting
    output_df.to_csv(file_path, index=False, decimal='.', float_format='%.2f')
    
    return file_path

def main():
    if len(sys.argv) != 2:
        print("Usage: python refunds_calcs.py path_to_folder")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    market_data_df = load_market_data(folder_path)
    pd.set_option('display.max_columns', None)
    print()
    print("-- Info for market_data_df ---")
    print()
    print(market_data_df.info())
    print()
    print("-- Head for market_data_df ---")
    print()
    print(market_data_df.head(10).to_string())
    print()
    print("-- Tail for market_data_df ---")
    print(market_data_df.tail(10).to_string())
    print()
    print("-- Executing stock performance calculation ---")
    stock_performance_df = calculate_stock_performance(market_data_df)
    print()
    print("-- Executing calc fund calculation ---")
    agg_df = calculate_fund_performance(fund_df, stock_performance_df)
    print()
    print("-- Executing cummulation ---")
    cu_fund_df = calculate_cumulative_fund_performance(agg_df)
    print()
    print("-- Info for users invested file ---")
    users_df = load_user_data(folder_path)
    print(users_df.info())
    print("-- Data for users invested file ---")
    print()
    print(users_df)
    print()
    print("-- Executing user refund calculation ---")
    print()
    output_df = calculate_user_refund(users_df,cu_fund_df)
    print()
    print("-- Output Table --")
    print(output_df.round(2))
    print()
    print("-- File path where file is exported --")
    export_to_csv(output_df, folder_path)
    print(export_to_csv(output_df, folder_path))
    
if __name__ == "__main__":
    main()

