import json
import klasa1
from datetime import datetime, timezone, timedelta
import MetaTrader5 as mt5
import klasa_enum
import sys
from colorama import init, Fore

"""
info
EAL z type_filling = FOK dzila sprawdzone


"""



init(autoreset=True)

def zlecenie(typ_, sl, tp, risk_usd, symbol):
    import MetaTrader5 as mt5

    mt5.symbol_select(symbol, True)
    info = mt5.symbol_info(symbol)
    tick = mt5.symbol_info_tick(symbol)

    if not info or not tick:
        raise RuntimeError("Brak danych symbolu")

    # 1️⃣ LOT SIZING
    lot = risk_usd / info.trade_contract_size
    lot = max(info.volume_min, min(lot, info.volume_max))
    lot = round(lot / info.volume_step) * info.volume_step
    lot = max(info.volume_min, lot)

    # 2️⃣ OFFSET pseudo-market (minimalny ruch w kierunku rynku)
    point = info.point
    offset = 2 * point

    # 3️⃣ USTALENIE CENY
    if typ_ == "LONG":
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask + offset
        if not (sl < price < tp):
            raise RuntimeError("Zla relacja SL/TP LONG")

    elif typ_ == "SHORT":
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid - offset
        if not (tp < price < sl):
            raise RuntimeError("Zla relacja SL/TP SHORT")

    else:
        raise RuntimeError("Nieznany typ")

    # 4️⃣ SPRAWDZENIE MINIMALNEJ ODLEGŁOŚCI SL/TP
    min_dist = info.trade_stops_level * point
    if abs(price - sl) < min_dist or abs(price - tp) < min_dist:
        raise RuntimeError("SL/TP zbyt blisko ceny")

    # 5️⃣ TWORZENIE ZLECENIA NATYCHMIASTOWEGO (DEAL) z FOK
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,  # FOK dla natychmiastowego wypełnienia
        "comment": "PSEUDO_MARKET",
    }

    result = mt5.order_send(request)
    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
        raise RuntimeError(result)

    return result.order


def zlecenie2(typ_, sl, tp, risk_usd, symbol):
    import MetaTrader5 as mt5

    mt5.symbol_select(symbol, True)
    info = mt5.symbol_info(symbol)
    tick = mt5.symbol_info_tick(symbol)

    if not info or not tick:
        raise RuntimeError("Brak danych symbolu")

    # 1️⃣ LOT SIZING
    lot = risk_usd / info.trade_contract_size
    lot = max(info.volume_min, min(lot, info.volume_max))
    lot = round(lot / info.volume_step) * info.volume_step
    lot = max(info.volume_min, lot)

    # 2️⃣ OFFSET pseudo-market (minimalny ruch w kierunku rynku)
    point = info.point
    offset = 2 * point

    # 3️⃣ USTALENIE CENY
    if typ_ == "LONG":
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask + offset
        if not (sl < price < tp):
            raise RuntimeError("Zla relacja SL/TP LONG")

    elif typ_ == "SHORT":
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid - offset
        if not (tp < price < sl):
            raise RuntimeError("Zla relacja SL/TP SHORT")

    else:
        raise RuntimeError("Nieznany typ")

    # 4️⃣ SPRAWDZENIE MINIMALNEJ ODLEGŁOŚCI SL/TP
    min_dist = info.trade_stops_level * point
    if abs(price - sl) < min_dist or abs(price - tp) < min_dist:
        raise RuntimeError("SL/TP zbyt blisko ceny")

    # 5️⃣ TWORZENIE ZLECENIA NATYCHMIASTOWEGO (DEAL) z FOK
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,  # FOK dla natychmiastowego wypełnienia
        "comment": "PSEUDO_MARKET",
    }

    result = mt5.order_send(request)
    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
        raise RuntimeError(result)

    return result.order

   



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
        print("################################################################################################################################################################################")
        print(f"czas : {datetime.now()}")

        instatncja.dane(1000)
       
        
        
        #instatncja.przeciecie(rodzaj_ema=200) # sprawdzamy ostania tu jest lookback+1 lookback=-1
        
       # zwroc_20=instatncja.dane_EMA_DO_PRZECIECIA(20)
       # zwroc_50=instatncja.dane_EMA_DO_PRZECIECIA(50)
       # sygnal=instatncja.sprawdz_cross_ema(zwroc_20, zwroc_50,look_back=0)
        
        if(sygnal!="NEUTRAL" and czy_zero_pozycji(mt5.positions_get())==1):
       

            instatncja.przeciecie(rodzaj_ema=200) 

            if(sygnal==instatncja.kierunek):

                

                if sygnal=="SHORT":
                    stop_loss=instatncja.stop_loss(1.5,"SHORT")
                    take_profit=instatncja.take_profit(1.5,"SHORT")
                    position_size=instatncja.R_multiple(zwroc_balans(mt5.account_info()), "SHORT", 1.5)

                else:
                    stop_loss=instatncja.stop_loss(1.5,"LONG")
                    take_profit=instatncja.take_profit(1.5,"LONG")
                    position_size=instatncja.R_multiple(zwroc_balans(mt5.account_info()), "LONG", 1.5)

                ticket=zlecenie(sygnal,stop_loss,take_profit,position_size,instatncja.symbol)
              
                instatncja.win_lose(ticket)
                print(Fore.YELLOW +f"wartosc aktulan swieczki - {instatncja.closees()[-1]}, wejscie  w pozycje {sygnal},czas =  {datetime.now()}")
                print(Fore.YELLOW +f" Stop Loss  : {stop_loss}")
                print(Fore.YELLOW +f"Take Profit   : {take_profit}")
                print(Fore.YELLOW +f"Position Size : {position_size}")
            
           
        
        
       



    

  

   