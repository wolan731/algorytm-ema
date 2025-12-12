import yfinance as yf
import pandas as pd 
import numpy as np
import string
import requests
import mod
from colorama import init, Fore, Back, Style
import json
init()
init(autoreset=True)


ticker = yf.Ticker("AAPL")





def main():
  mod.info(ticker)

main()