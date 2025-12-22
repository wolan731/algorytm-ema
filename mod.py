import json
import klasa1
from datetime import datetime, timezone, timedelta
import MetaTrader5 as mt5
import klasa_enum
import sys


def zlecenie( typ_ :str,sl,tp,position_size_usd,symbol):
    
    lot = position_size_usd / 100000
    if(typ_=="Long"):
        request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(symbol).ask,
        "sl": sl,
        "tp": tp,
        "deviation": 20,  
        "magic": 123456,  
        "comment": "algo test",
        "type_time": mt5.ORDER_TIME_GTC,  # good till canceled
        "type_filling": mt5.ORDER_FILLING_IOC,
        }
    if(typ_=="Short"):
        request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(symbol).ask,
        "sl": sl,
        "tp": tp,
        "deviation": 20,  
        "magic": 123456, 
        "comment": "algo test",
        "type_time": mt5.ORDER_TIME_GTC,  # good till canceled
        "type_filling": mt5.ORDER_FILLING_IOC,
        }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Blad wysylki:", result)
    else:
        print("Zlecenie wyslane:", result)
    
   



def info_mt5():
            if not mt5.initialize():
                print("Blad polaczenia:", mt5.last_error())
                return None
            else:
                       
                     print("Polaczono z MT5!")
                     account = mt5.account_info()
                     
                     if account is not None:
                         print("Login:", account.login)
                         print("Broker:", account.server)
                         print("Saldo:", account.balance)
                         print("Dzwignia:", account.leverage)
                         return account
                     else:
                         print("Nie udalo sie pobrac informacji o koncie")
                         return None

def main_info():
            if not mt5.initialize():
                        print("Blad polaczenia:", mt5.last_error())
                        return None
            else:
                       
                             print("Polaczono z MT5!")
                             account = mt5.account_info()
                             mt5.shutdown()
                             return account
                             

def londondon_newyork():
     now_utc = datetime.now(timezone.utc)
     hour_utc = now_utc.hour
     return 8 <= hour_utc < 21


def czy_zero_pozycji(pozycja):
    if(pozycja==1):
        return 0
    else:
        return 1

def zwroc_balans(account):
        
        return account.balance
   

def info(stop_price_cross_ema :int,stop_ema_cross_ema: int ,instatncja : klasa1.dane_glowne_MT5):
   
        

        mt5.initialize() #mt5.initializacja
        
        instatncja.dane(1000)
       
        #print(instatncja.atr(14))
        #print(instatncja.dane_EMA_SMA_SPADKOWY_WZROSTOWY(50))
    
        instatncja.przeciecie(rodzaj_ema=200,lookback=1) # sprawdzamy ostania tu jest lookback+1 lookback=-1
        #print(czy_zero_pozycji(mt5.positions_get()))
        if(instatncja.kierunek!="NEUTRAL" and czy_zero_pozycji(mt5.positions_get())==1):
       
            zwroc_20=instatncja.dane_EMA_DO_PRZECIECIA(20)
            zwroc_50=instatncja.dane_EMA_DO_PRZECIECIA(50)
            sygnal=instatncja.sprawdz_cross_ema(zwroc_20, zwroc_50,look_back=0)
           

            if(sygnal==instatncja.kierunek):

                

                if sygnal=="SHORT":
                    stop_loss=instatncja.stop_loss(1.5,"SHORT")
                    take_profit=instatncja.take_profit(1.5,"SHORT")
                    position_size=instatncja.R_multiple(zwroc_balans(mt5.account_info()), "SHORT", 1.5)
                else:
                    stop_loss=instatncja.stop_loss(1.5,"LONG")
                    take_profit=instatncja.take_profit(1.5,"LONG")
                    position_size=instatncja.R_multiple(zwroc_balans(mt5.account_info()), "LONG", 1.5)

                print(f"{instatncja.closees()[-1]}, wejscie  w pozycje {sygnal},czas =  {datetime.now()}")
                print(f"Stop Loss     : {stop_loss}")
                print(f"Take Profit   : {take_profit}")
                print(f"Position Size : {position_size}")
            
           
        
        
            """   
            
                 print("wchodzi")
                 if(signal==klasa_enum.Kierunek.SHORT) or (stop_ema_cross_ema==klasa_enum.Kierunek.SHORT):
                    print("short wchodzi")
                    stop_loss=dzien.stop_loss(1.5,"Short")
                    take_profit=dzien.take_profit(1.5,"Short")
                    position_size=dzien.R_multiple(zwroc_balans(accont), "Short", 1.5)
                    #zlecenie( "Short",stop_loss,take_profit,position_size,"GBPUSD")
               
                    return 

                 if(signal==klasa_enum.Kierunek.LONG) or (stop_ema_cross_ema==klasa_enum.Kierunek.LONG):
                    print("long wchodzi")
                    stop_loss=dzien.stop_loss(1.5,"Long")
                    take_profit=dzien.take_profit(1.5,"Long")
                    position_size=dzien.R_multiple(zwroc_balans(accont), "Long", 1.5)
                    #zlecenie("Long",stop_loss,take_profit,position_size,"GBPUSD")
                   

                    return  
            """
        



    

  

   