import requests
import concurrent.futures
import pandas as pd
import time
import pygsheets
from datetime import datetime

def fetch_option_data(option):
    # Function to fetch data for a single option
    return {
        'calls_oi': option['calls_oi'],
        'calls_change_oi': option['calls_change_oi'],
        'calls_volume': option['calls_volume'],
        'calls_ltp': option['calls_ltp'],
        'calls_net_change': option['calls_net_change'],
        'calls_iv': option['calls_iv'],
        'calls_open': option['call_open'],
        'calls_high': option['call_high'],
        'calls_low': option['call_low'],
        'strike_price': option['strike_price'],
        'puts_oi': option['puts_oi'],
        'puts_change_oi': option['puts_change_oi'],
        'puts_volume': option['puts_volume'],
        'puts_ltp': option['puts_ltp'],
        'puts_net_change': option['puts_net_change'],
        'puts_iv': option['puts_iv'],
        'puts_open': option['put_open'],
        'puts_high': option['put_high'],
        'puts_low': option['put_low'],
        'spotprice': option['index_close'],
  # Added symbol_name to extract the symbol name
    }

def fetch_option_chain_data(api_url):
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        op_datas = data['resultData']['opDatas']

        # Use ThreadPoolExecutor to parallelize the API requests
        with concurrent.futures.ThreadPoolExecutor() as executor:
            options_data = list(executor.map(fetch_option_data, op_datas))

        # Creating a DataFrame
        df = pd.DataFrame(options_data)

        return df
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def run_program(url_info):
    api_url = url_info['api_url']

    option_chain_df = fetch_option_chain_data(api_url)

    if option_chain_df is not None:
        print(option_chain_df)
        gc = pygsheets.authorize(service_account_file='creds1.json')
        sh = gc.open('option_data')  # Replace with your actual Google Sheets document name

        # Map predefined names to URLs
        predefined_symbol_names = {
           
            'https://webapi.niftytrader.in/webapi/option/fatch-option-chain?symbol=nifty&expiryDate=': 'nityprice',
            # Add more mappings for additional URLs
        }

        # Extract the URL from the dictionary
        current_url = url_info['api_url']

        # Extract the predefined symbol name or use the URL as a fallback
        symbol_name = predefined_symbol_names.get(current_url, current_url)

        # Find the worksheet with the same symbol name
        worksheet = sh.worksheet_by_title(symbol_name)

        if worksheet:
            # If the worksheet exists, update its content
            worksheet.set_dataframe(option_chain_df, (1, 1))
            print(f'Data updated for {symbol_name} successfully')
        else:
            # If the worksheet doesn't exist, create a new worksheet
            new_worksheet = sh.add_worksheet(symbol_name)
            new_worksheet.set_dataframe(option_chain_df, (1, 1))
            print(f'Data recorded for {symbol_name} successfully')

# List of URLs
url_infos = [
     {'api_url': 'https://webapi.niftytrader.in/webapi/option/fatch-option-chain?symbol=nifty&expiryDate='},
    # Add more dictionaries for additional URLs
]


# Run the program every 20 seconds for each URL
while True:
    for url_info in url_infos:
        run_program(url_info)
    time.sleep(50)

