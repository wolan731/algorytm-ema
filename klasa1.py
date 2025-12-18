from abc import update_abstractmethods
import json
from typing import Self
import pandas
import numpy
from pandas._libs import interval
import yfinance as yf
import MetaTrader5 as mt5
class dane_glowne:

    _instance = None






























  
    def sprawdz_cross_ema(self,zwroc_20:list,zwroc_50:list):
        EPS = 1e-5  # bufor anty-szumowy

        diff_prev = zwroc_20[0] - zwroc_50[0]
        diff_curr = zwroc_20[1] - zwroc_50[1]
       
        if diff_prev < -EPS and diff_curr > EPS:
            
            print("📈 GOLDEN CROSS (EMA20 ↑ EMA50)")
            return 1

        elif diff_prev > EPS and diff_curr < -EPS:
       
            print("📉 DEATH CROSS (EMA20 ↓ EMA50)")
            return 1

        else:
            
            print("Brak crossa")























    def SMA_START(self,close_values : pandas.DataFrame,okres):
         
            
          

      

            if(len(close_values) < okres):
                print("Za malo danych: lista close_values ma mniej niz 50 elementow. Nie mozna obliczyc SMA50.")
                raise ValueError("Za malo danych: lista close_values ma mniej niz 50 elementow. Nie mozna obliczyc SMA50.")
               

            self.sma=0

            self.sma = sum(close_values[:okres]) / okres
            return self.sma



    def przeciecie(self, zwroc):
        EPS = 1e-4

        ema_prev   = zwroc[0]
        ema_curr   = zwroc[1]
        price_prev = zwroc[2]
        price_curr = zwroc[3]

        diff_prev = price_prev - ema_prev
        diff_curr = price_curr - ema_curr

        if diff_prev < -EPS and diff_curr > EPS:
           
           print("EMA przecinana od dołu (wzrostowe)")
           return 1
        elif diff_prev > EPS and diff_curr < -EPS:
          
            print("EMA przecinana od góry (spadkowe)")
            return 1
        else:
            print("Brak przecięcia")
            
            


                                                            
    def closees(self,ticker: yf.Ticker,period: int,time_frame: int):
    
         df=ticker.history(
            period=period,
            interval=time_frame
            )

         close_values = df["Close"].tolist()
         return close_values

    
    def dane_EMA_SMA_SPADKOWY_WZROSTOWY(self,ticker: yf.Ticker,ema_okres :int ,period_of_data :str,time_frame: int):
        ema_values=[]
        okres=ema_okres
        wspolczynik_wygladzenia=2/(okres+1)

        


        close_values = self.closees(ticker,period_of_data,time_frame)
        

        up=None
        down=None

      #  self.ema=0
        self.ema = self.SMA_START(close_values,okres)
        ema_values.append(self.ema)
      

        for index,zamkniecie in enumerate(close_values[okres:]):
            
            self.ema=float(zamkniecie)*wspolczynik_wygladzenia+self.ema*(1-wspolczynik_wygladzenia)
            ema_values.append(self.ema)

        if len(ema_values) < 2:
         print("Za malo wartosci EMA, zwracam testową liste")
         return [0, 0, 0, 0]
        
        self.price_prev = close_values[-2]
        self.price_curr = close_values[-1]

        self.ema_prev = ema_values[-2]
        self.ema_curr = ema_values[-1]

        ema_values_zwroc=[self.ema_prev, self.ema_curr]
        price_values_zwroc=[ self.price_prev,self.price_curr]
        zwroc=[]
        zwroc.extend(ema_values_zwroc)
        zwroc.extend(price_values_zwroc)

        return (zwroc)
        #######################
       
        
       







    def __new__(cls, ticker: yf.Ticker):
        if cls._instance is None:
            if not mt5.initialize():
                print("Błąd połączenia:", mt5.last_error())
            else:
                print("Połączono z MT5!")
            cls._instance = super().__new__(cls)
        return cls._instance

   

    def __init__(self, ticker: yf.Ticker):
        
        info = ticker.info
     
        self.day_low = info.get("dayLow")
        self.day_high = info.get("dayHigh")
        self.open_price = info.get("open")
        self.close_price = info.get("previousClose")
        

   
    
 




