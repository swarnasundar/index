import logging
import time
from datetime import datetime, timedelta
import pygsheets
import pandas as pd
import schedule
from pytz import timezone

def datafetch():
    a= 5
    b= 4
    c= a+b
    print(c)

while True:
    datafetch()
    time.sleep(5)

