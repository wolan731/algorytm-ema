import json
import yfinance as yf
import klasa1
def info(ticker: yf.Ticker ):
    dzien=klasa1.dane_glowne(ticker)
    