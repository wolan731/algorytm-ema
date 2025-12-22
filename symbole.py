import MetaTrader5 as mt5

mt5.initialize()

symbols = mt5.symbols_get()
crypto_symbols = [s.name for s in symbols if any(c in s.name for c in ["BTC","ETH","DOGE","XRP","ADA"])]
print(crypto_symbols)

