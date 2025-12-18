import json
import yfinance as yf
import klasa1
import datetime


def info(ticker: yf.Ticker,stop_price_cross_ema :int,stop_ema_cross_ema: int ):
    dzien=klasa1.dane_glowne(ticker)
    
  
    stop_price_cross_ema=dzien.przeciecie(dzien.dane_EMA_SMA_SPADKOWY_WZROSTOWY(ticker,50,"1d","1m"))
    stop_ema_cross_ema=dzien.sprawdz_cross_ema(dzien.dane_EMA_SMA_SPADKOWY_WZROSTOWY(ticker,20,"1d","1m"),dzien.dane_EMA_SMA_SPADKOWY_WZROSTOWY(ticker,50,"1d","1m"))
   

  

    if stop_price_cross_ema or stop_ema_cross_ema ==1:
        print(datetime.datetime.now())
        print("####################################")
        input("Wcisnij ENTER, aby kontynuowac...")