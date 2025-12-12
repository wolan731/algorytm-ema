import yfinance as yf
import pandas as pd 
import numpy as np
import string
import requests
from colorama import init, Fore, Back, Style
import json
init()
init(autoreset=True)

zmienna="AAPL"






def main():
    apple,dane=wczytaj("1d","15m")
    last_hour=wypisz(apple,dane)
    analizuj3swiece(last_hour)

main()