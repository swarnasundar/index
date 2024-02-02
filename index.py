import streamlit as st
import logging
import time
from datetime import datetime, timedelta
import pygsheets
import pandas as pd
import schedule
from pytz import timezone

logging.basicConfig(filename='app.log', level=logging.INFO)

def get_previous_weekday(date, holiday_list):
    while date.weekday() > 4 or date.strftime("%Y-%m-%d") in holiday_list:
        date -= timedelta(days=1)
    return date
global weeklyexpiry

# Read the holiday list from CSV
holidays = pd.read_csv('holidays.csv')
dates_list = holidays['Day'].tolist()

# Get the current date and find the next Thursday
today = datetime.today()
weeklyexpiry = today + timedelta(days=(3 - today.weekday() + 7) % 7)

# Check if the expiry date is a holiday or weekend, and find the previous valid weekday


# Find the first day of the next month

# Calculate the last day of the current month by subtracting one day from the first day of the next month


# Calculate the weekday of the last day of the current month (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)


bnfexpiry = today + timedelta(days=(2 - today.weekday() + 7) % 7)

# Check if the expiry date is a holiday or weekend, and find the previous valid weekday
weeklyexpiry = get_previous_weekday(weeklyexpiry, dates_list)
bnfexpiry = get_previous_weekday(bnfexpiry, dates_list)
weeklyexpiry=weeklyexpiry.strftime("%Y-%m-%d")
bnfexpiry=bnfexpiry.strftime("%Y-%m-%d")

# Print the result
print(bnfexpiry+weeklyexpiry)

def fetch_data(url):
    try:
        df = pd.read_html(url)[0]
        df.replace('-', '0', inplace=True)
        return df
    except Exception as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None

def update_google_sheets(gc, sheet_name, dataframe):
    try:
        sh = gc.open(sheet_name)
        worksheet = sh[0]
        worksheet.set_dataframe(dataframe, (2, 1))
        logging.info(f"Data updated successfully in Google Sheets ({sheet_name}).")
    except Exception as e:
        logging.error(f"Error updating Google Sheets ({sheet_name}): {e}")

def datafetch():
    try:
        nftdf1 = pd.read_html(f'https://www.moneycontrol.com/india/indexfutures/nifty/9/{weeklyexpiry}/OPTIDX/CE/18500.00/true')
        nftresult = nftdf1[4]
        #nftresult
        nftresult2= nftresult.replace('-','0')
        nftdf2 = pd.read_html('https://www.moneycontrol.com/india/indexfutures/nifty/9/2022-06-02/OPTIDX/CE/14300.00/true')
        nftresult1=nftdf2[0]
        #nftresult2.to_csv('nftoc.csv',index=False,header=True)
        niftyspot = nftresult1.iat[4,1]
        bnfdf1 = pd.read_html(f'https://www.moneycontrol.com/india/indexfutures/banknifty/23/{bnfexpiry}/OPTIDX/CE/43900.00/true')
        bnfresult = bnfdf1[4]
        #bnfresult
        bnfresult2= bnfresult.replace('-','0')
        bnfdf2 = pd.read_html('https://www.moneycontrol.com/india/indexfutures/banknifty/23/2022-06-09/OPTIDX/CE/28900.00/true')
        bnfresult1=bnfdf2[0]
        bankniftyspot = bnfresult1.iat[4,1]
        now = datetime.now(timezone('Asia/Kolkata'))
        current_time = now.strftime("%H:%M:%S")
        current_time
        frames =[nftresult2,nftresult1]
        result = pd.concat([nftresult2,nftresult1],axis=1)
        result1 = pd.concat([bnfresult2,bnfresult1],axis=1)

        #nftresult1 =nftresult.sort_values(by=['CHANGEOIPER'])
        #print(nftresult1)
        print(result)
        #nftresult2 = pd.read_csv('nftoc.csv')
        path=r'C:\Users\SMAA\creds1.json'
        gc=pygsheets.authorize(service_account_file='creds1.json')
        sh=gc.open('NFTSOURCE2109')
        wk1=sh[0]
        wk2=sh[1]
        wk3=sh[2]
        wk1.set_dataframe(result,(2,1))
        wk2.set_dataframe(result1,(2,1))
        print(current_time+' '+'DATA RECORDED SUCCESSFULLY')
    #schedule.every(1).minutes.do(datafetch)

        now = datetime.now(timezone('Asia/Kolkata'))
        current_time = now.strftime("%H:%M:%S")
        logging.info(f"{current_time} - Data recorded successfully.")
    except Exception as e:
        logging.error(f"Error in datafetch: {e}")
        raise  # Re-raise the exception to restart the program

if __name__ == "__main__":
    gc = pygsheets.authorize(service_account_file='creds1.json')

    while True:
        try:
            datafetch()
            time.sleep(5)
        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
