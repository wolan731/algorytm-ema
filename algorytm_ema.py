import yfinance as yf
import pandas as pd 
import numpy as np
import string
import requests
import mod
import json
import time
import MetaTrader5 as mt5
import klasa1
import klasa_enum
from datetime import datetime, timedelta








time.sleep(1)
symbol="USDJPY"
dane=klasa1.dane_glowne_MT5(symbol)

def wait_60_seconds_aligned(): #prawidlowy
    now = datetime.now()
    next_time = now + timedelta(seconds=60)
    sleep_time = (next_time - now).total_seconds()
    time.sleep(sleep_time)



def main():
   
    mt5.initialize()

    
   
    
    stop_price_cross_ema=0 
    stop_ema_cross_ema=0
    while(1):
        #if mod.londondon_newyork():
             
             mod.info(stop_price_cross_ema,stop_ema_cross_ema,dane) #prawidlowy
             wait_60_seconds_aligned()
       # else:
           # time.sleep(10*60)
    
    

main()