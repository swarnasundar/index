import streamlit as st
import json
from pytz import timezone 
import pandas as pd
import numpy as np
import time
from datetime import datetime,timedelta,date
import pygsheets
import calendar
import pyrebase
def datafetch():
    firebaseConfig ={"apiKey": "AIzaSyDRCNxFhkbWwjanpPBGLBb7plPISrnhowU",
    "authDomain": "dash-92a7e.firebaseapp.com",
    "databaseURL": "https://dash-92a7e-default-rtdb.firebaseio.com/",
    "projectId": "dash-92a7e",
    "storageBucket": "dash-92a7e.appspot.com",
    "messagingSenderId": "365112842534",
    "appId": "1:365112842534:web:e3805cc81ad2a4c15309e7",
    "measurementId": "G-T4KZ8VJ8JT"}
    
    firebase=pyrebase.initialize_app(firebaseConfig)
    db=firebase.database()
    path=r'C:\Users\SMAA\creds1.json'
    gc=pygsheets.authorize(service_account_file='creds1.json')
    sh=gc.open('HEADER')
    #sh1=gc.open('BNFSOURCE2606')
    #sh2=gc.open('FUTURESCREENER')
    wk1=sh[1]
    nft=wk1.get_as_df(start='A1',end='B23')
    nfttrend = nft.iloc[0,1]
    nftspot = nft.iloc[1,1]
    nftmaxpain = nft.iloc[2,1]
    nftnetchange = nft.iloc[3,1]
    nftdemand = nft.iloc[4,1]
    nftsupply = nft.iloc[5,1]
    nftceprem= nft.iloc[6,1]
    nftpeprem= nft.iloc[7,1]
    nftintratrend= nft.iloc[8,1]
    nftcebuypoints= nft.iloc[9,1]
    nftpebuypoints=nft.iloc[10,1]
    bnfttrend = nft.iloc[11,1]
    bnftspot = nft.iloc[12,1]
    bnftmaxpain = nft.iloc[13,1]
    bnftnetchange = nft.iloc[14,1]
    bnftdemand = nft.iloc[15,1]
    bnftsupply = nft.iloc[16,1]
    bnftceprem= nft.iloc[17,1]
    bnftpeprem= nft.iloc[18,1]
    bnftintratrend= nft.iloc[19,1]
    bnftcebuypoints= nft.iloc[20,1]
    bnftpebuypoints=nft.iloc[21,1]
    #print(print1)
    #wk2=sh1[0]
    #wk3=sh2[0]
    #celtp = result['celtp']
    #ceprchng = result['ceprchng']
    #nfttrend = nfttrend.to_json()
    #niftyspot = nftspot.to_json()
    #json= result.to_json()
    #print(json)
    print(nftspot)
    nifty={"niftyspot":nftspot,"niftytrend":nfttrend,"niftynetchange":nftnetchange,"niftymaxpain":nftmaxpain,"niftydemand":nftdemand,"niftysupply":nftsupply,"niftyceprem":nftceprem,"niftypeprem":nftpeprem,"nftintratrend":nftintratrend,"nftcebuypoints":nftcebuypoints,"nftpebuypoints":nftpebuypoints,"bniftyspot":bnftspot,"bniftytrend":bnfttrend,"bniftynetchange":bnftnetchange,"bniftymaxpain":bnftmaxpain,"bniftydemand":bnftdemand,"bniftysupply":bnftsupply,"bniftyceprem":bnftceprem,"bniftypeprem":bnftpeprem,"bnftintratrend":bnftintratrend,"bnftcebuypoints":bnftcebuypoints,"bnftpebuypoints":bnftpebuypoints}
    #niftytrend={"niftytrend":nfttrend}
    #db.update(data)
    db.update(nifty)
    print(nifty)
    #db.child('nifty').update({"niftyspot":niftyspot})
    #db.child('nifty').update({"ceprchng":ceprchng})
    #db.update(json)
    #wk1.set_dataframe(result,(2,1))
    #wk2.set_dataframe(result1,(2,1))
    #wk3.set_dataframe(nftsresult,(1,1))
    #print(current_time+' '+'DATA RECORDED SUCCESSFULLY')
    #schedule.every(1).minutes.do(datafetch)
    #schedule.every(1).minutes.do(nft2gsheet)
while True:
    datafetch()
    time.sleep(5)
  
