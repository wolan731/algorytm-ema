import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import math
import klasa_enum
from datetime import datetime , timedelta,timezone 
from colorama import init, Fore
#abs(EMA20 - EMA50) > X dodaj dystans

class dane_glowne_MT5:

    _instance = None
    


    def __new__(cls,symbol: str): # prowidlowy 
        if cls._instance is None:
            cls._instance = super().__new__(cls)
           
        return cls._instance

    def __init__(self,symbol: str): # prowidlowy 
        self.symbol = symbol
        init(autoreset=True)
        
     
        self.zmiana=0
        self.lose = 0
        self.kierunek="NEUTRAL"
        

    # ---------------- Dane ----------------

    def dane(self, lookback: int, timeframe=mt5.TIMEFRAME_M1): # prowidlowy 
        info = mt5.symbol_info(self.symbol)
        if info is None:
            raise RuntimeError(
                "MT5 nie zwraca symbol_info – "
                "terminal nie jest zalogowany lub nie działa"
            )

        rates = mt5.copy_rates_from_pos(
            self.symbol, timeframe, 1, lookback
        )

        if rates is None or len(rates) < lookback:
            raise RuntimeError(mt5.last_error())

        
        self.df = pd.DataFrame(rates)
        
        pd.set_option('display.max_columns', None)
      #  print(self.df)
        self.df["time"] = pd.to_datetime(self.df["time"], unit="s")
        print(self.df.iloc[-1])
      #  last_close = self.df.iloc[-1]["close"]
      #  print(f"Last closed candle close price: {last_close}")
        
    
    def closees(self):
         return self.df["close"].tolist() # prowidlowy 
    
    def opens(self):
            return self.df["open"].tolist() # prowidlowy 

    def highs(self):
            return self.df["high"].tolist() # prowidlowy 

    def lows(self): 
            return self.df["low"].tolist() # prowidlowy 

        # ---------------- ATR, Stop Loss, Take Profit ----------------
         
    def atr(self, n):                                        # prowidlowy
            close = self.closees()  
            high = self.highs()
            low = self.lows()

            if len(close) < n + 1:
                raise ValueError(f"Za mało danych do ATR (min {n+1} świec)")

            # Oblicz TR dla wszystkich świec (od 1 do końca)
            TR_list = [
                max(
                    high[i] - low[i],
                    abs(high[i] - close[i-1]),
                    abs(low[i] - close[i-1])
                )
                for i in range(1, len(close))
            ]

            # ATR początkowy = SMA z pierwszych n TR
            atr = sum(TR_list[:n]) / n

            # Wygładzanie RMA / Wilder
            for TR in TR_list[n:]:
                atr = (atr * (n - 1) + TR) / n

            return atr
   
    def stop_loss(self, k: float, czyn: str):
            if czyn == "SHORT":
                return self.closees()[-1] + k * self.atr(14)
            return self.closees()[-1] - k * self.atr(14)

    def take_profit(self, k: float, czyn: str):
            if czyn == "SHORT":
                return self.closees()[-1] - k * self.atr(14)
            return self.closees()[-1] + k * self.atr(14)

    def R_multiple(self, capital: float, side: str, atr_multiplier: float = 1.5):
            risk_percent = self.risk_leader()
            entry = self.closees()[-1]
            SL = self.stop_loss(atr_multiplier, side)
            risk_per_unit = abs(entry - SL)
            if risk_per_unit == 0 or capital is None:
                return 0
            return (capital * risk_percent) / risk_per_unit

    def win_lose(self, ticket):
        if ticket is None:
            print(Fore.RED + "Błąd: brak numeru ticket")
            return

        utc_to = datetime.now(timezone.utc)
        utc_from = utc_to - timedelta(hours=24)

        history_positions = mt5.history_deals_get(utc_from, utc_to, ticket)

        if history_positions is None:
            print(Fore.RED + "Błąd: brak danych historycznych")
            return

        for pos in history_positions:
           # print(f"Ticket: {pos.ticket}, Type: {pos.type}, Profit: {pos.profit}")

            if pos.profit > 0:
               # print(Fore.CYAN + "WYGRANA")
                self.lose = 0

            elif pos.profit < 0:
               # print(Fore.CYAN + "STRATA")
                self.lose += 1

            
               # print(Fore.CYAN + "BREAK EVEN")


    def risk_leader(self):
            if self.lose == 0: return 0.05
            if self.lose == 1: return 0.025
            if self.lose == 2: return 0.015
            if self.lose >= 3: return 0.01

        # ---------------- EMA, SMA, Przecięcia ----------------
     
    def SMA_START(self, close_values, okres):
            if len(close_values) < okres:
                raise ValueError(f"Za mało danych: {len(close_values)} < {okres}")
            self.sma = sum(close_values[:okres]) / okres
            return self.sma

    def dane_EMA_SMA_SPADKOWY_WZROSTOWY(self, ema_okres: int)-> int: # prowidlowy
            ema_values = []
            okres = ema_okres
            wspolczynik_wygladzenia = 2 / (okres + 1)
            self.ema_values=[]
            print(self.closees()[-1])
            close_values = self.closees()
            self.ema = self.SMA_START(close_values, okres)
            self.ema_values.append(self.ema)

            for zamkniecie in close_values[okres:]:
                self.ema = float(zamkniecie)*wspolczynik_wygladzenia + self.ema*(1-wspolczynik_wygladzenia)
                self.ema_values.append(self.ema)

            return self.ema

    def dane_EMA_DO_PRZECIECIA(self, ema_okres: int)-> int:  # prowidlowy
            
            okres = ema_okres
            wspolczynik_wygladzenia = 2 / (okres + 1)
            self.ema_values_PRZECIECIA=[]
            close_values = self.closees()
            self.ema_PRZECIECIA = self.SMA_START(close_values, okres)
            self.ema_values_PRZECIECIA.append(self.ema_PRZECIECIA)

            for zamkniecie in close_values[okres:]:
                self.ema_PRZECIECIA = float(zamkniecie)*wspolczynik_wygladzenia + self.ema_PRZECIECIA*(1-wspolczynik_wygladzenia)
                self.ema_values_PRZECIECIA.append(self.ema_PRZECIECIA)

            return self.ema_values_PRZECIECIA
    
    def przeciecie(self,  rodzaj_ema,lookback=1)-> None:  # prowidlowy
        EPS = 1e-4
        close_values = self.closees()
        ema_values = self.dane_EMA_DO_PRZECIECIA(rodzaj_ema)

        shift = len(close_values) - len(ema_values)
        start = max(shift + 1, len(close_values) - lookback)
        
     
        for i in range(start, len(close_values)):
           
            diff_prev = close_values[i-1] - ema_values[i-1-shift]
            diff_curr = close_values[i]   - ema_values[i-shift]

            if diff_prev < -EPS and diff_curr > EPS: 
                print(Fore.GREEN + f" LONG | świeca i={i} (od końca {- (len(close_values)-i)}) | "
                        f"close={close_values[i]:.5f} | ema={ema_values[i-shift]:.5f}")
                self.kierunek="LONG"
                return 

            if diff_prev > EPS and diff_curr < -EPS:
                print(Fore.RED +f"SHORT | świeca i={i} (od końca {- (len(close_values)-i)}) | "
                        f"close={close_values[i]:.5f} | ema={ema_values[i-shift]:.5f}")
                self.kierunek="SHORT"
                return 
              
        print(Fore.BLUE + f"NEUTRAL | ostatnia świeca | "
        f"close={close_values[-1]:.5f} | ema={ema_values[-1]:.5f}")
        
        self.kierunek="NEUTRAL"
        return 
    # ---------------- Cross EMA ----------------

    def sprawdz_cross_ema(self, zwroc_20: list, zwroc_50: list, look_back=0) -> str:
        EPS = 1e-5

        diff_prev = zwroc_20[-2] - zwroc_50[-2]
        diff_curr = zwroc_20[-1] - zwroc_50[-1]

        if diff_prev < -EPS and diff_curr > EPS:
            print(Fore.GREEN + f"GOLDEN CROSS  EMA20 > EMA50  -> LONG {self.closees()[-1]}")
            self.zmiana = 1
            return "LONG"

        elif diff_prev > EPS and diff_curr < -EPS:
            print(Fore.RED + f"DEATH CROSS   EMA20 < EMA50  -> SHORT {self.closees()[-1]}")
            self.zmiana = 1
            return "SHORT"

        print(Fore.BLUE + f"NO CROSS      EMA20 ~ EMA50  -> NEUTRAL {self.closees()[-1]}")

        if self.zmiana == 0:
            return "NEUTRAL"
        
       
      
  
