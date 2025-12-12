from abc import update_abstractmethods
import json
import pandas
import numpy
from pandas._libs import interval
import yfinance as yf
class dane_glowne:

    _instance = None
    def SMA_START(self,ticker: yf.Ticker):
            df=ticker.history(
            period="10d",
            interval="4h"
            )
            okres=50
            df_ostatnie_50 = df.tail(okres)

            
            close_values=df["Close"].tolist()
            
            self.sma=0

            for zamkniecie in close_values:
                 self.sma= self.sma+zamkniecie
            self.sma= self.sma/okres
            return self.sma




    
    def dane_EMA_SMA_SPADKOWY_WZROSTOWY(self,ticker: yf.Ticker):
        
        okres=50
        wspolczynik_wygladzenia=2/(okres+1)

        df=ticker.history(
            period="10d",
            interval="4h"
            )
        df_ostatnie_50 = df.tail(okres)
        ostatnia_swieca = df.tail(1)
         
        
        close_values=df["Close"].tolist()
        open_values=df["Open"].tolist()

        up=None
        down=None
        self.ema=ostatnia_swieca["Close"].tolist()*wspolczynik_wygladzenia+self.SMA_STAR(ticker)*(1-wspolczynik_wygladzenia)

        for zamkniecie in close_values:
            self.ema=ostatnia_swieca["Close"].tolist()*wspolczynik_wygladzenia+self.ema*(1-wspolczynik_wygladzenia)
        return self.ema

        """
        for otwarcie,zamkniecie in open_values,close_values:
            r=otwarcie-zamkniecie
            if(r>0):
                down+=1
            else:
                up+=1
                """




    def __new__(cls, ticker: yf.Ticker):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

   

    def __init__(self, ticker: yf.Ticker):
        
        info = ticker.info
        self.dane_EMA_SMA_SPADKOWY_WZROSTOWY(ticker)
        self.day_low = info.get("dayLow")
        self.day_high = info.get("dayHigh")
        self.open_price = info.get("open")
        self.close_price = info.get("previousClose")
        

   
    
 




