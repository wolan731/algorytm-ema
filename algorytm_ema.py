import yfinance as yf
import pandas as pd 
import numpy as np
import string
import requests
import mod
from colorama import init, Fore, Back, Style
import json
import time
from datetime import datetime, timedelta
init()
init(autoreset=True)


ticker = yf.Ticker("GBPUSD=X")

def wait_until_next_minute():
    time.sleep(10)
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    time.sleep((next_minute - now).total_seconds())



def main():
   
    stop_price_cross_ema=0
    stop_ema_cross_ema=0
    while(1):
     wait_until_next_minute()
     mod.info(ticker,stop_price_cross_ema,stop_ema_cross_ema)
     

main()