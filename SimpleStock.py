from datetime import datetime
from functools import reduce
from random import random, randint, normalvariate
from time import time
from math import pow
from operator import mul

AvgTradePerSec = 10
RecordingTime = 15 * 60
result = []

def recordTrade(Stock, timestamp):
    change = normalvariate(random(), 10)
    MarketPrice = int(Stock["ParValue"] + change)
    return {'timestamp': datetime.fromtimestamp(timestamp + change).isoformat(),
            'buy/sell': 'buy' if MarketPrice < Stock["ParValue"] else 'sell',
            'amount': randint(0, 100000),
            'price': MarketPrice}

def recordTrades(Stock):
    timestamp = time()
    for i in range(RecordingTime * AvgTradePerSec):
        timestamp = timestamp-(1.0 / AvgTradePerSec)
        result.append(recordTrade(Stock, timestamp))
    return result

def dividendYield(Stock):
    common = float(Stock["LastDividend"]) / Stock["MarketPrice"]
    preferred = float(Stock["FixedDividend"] * Stock["ParValue"]) / Stock["MarketPrice"]
    return {"CommonDY": common, "PreferredDY": preferred}

def pE(Stock):
    return(float(Stock["MarketPrice"]) / Stock["LastDividend"] if Stock["LastDividend"] else "None")

def stockPrice(trades):
    sum_values = sum(map(lambda x: float(x['amount']) * x['price'], trades))
    sum_amount = sum(map(lambda x: float(x['amount']), trades))
    return sum_values / sum_amount

def geometricMean(Stock):
    prices = map(lambda x: x["MarketPrice"], Stock)
    product = reduce(mul, prices)
    return pow(product, 1 / float(len(Stock)))


Stock = [{'StockSymbol':'TEA', 'Type': 'Common', 'LastDividend': 0.0, 'FixedDividend':0.0,'ParValue': 100},
          {'StockSymbol':'POP', 'Type': 'Common', 'LastDividend': 8.0, 'FixedDividend':0.0,'ParValue': 100},
          {'StockSymbol':'ALE', 'Type': 'Common', 'LastDividend': 23.0, 'FixedDividend':0.0,'ParValue': 60},
          {'StockSymbol':'GIN', 'Type': 'Preferred', 'LastDividend': 8.0, 'FixedDividend':2.0,'ParValue': 100},
          {'StockSymbol':'JOE', 'Type': 'Common', 'LastDividend': 13.0, 'FixedDividend':0.0,'ParValue': 250}]


print(' ')
print()
print("\t| ".join(["StockSymbol", "MarketPrice", "pe_ratio", "dividend_Yield"]))
for i in range(5):
    Stock[i]["MarketPrice"] = stockPrice(recordTrades(Stock[i]))
    print()
    print("\t|".join([Stock[i]["StockSymbol"], str(Stock[i]["MarketPrice"]), str(pE(Stock[i])), str(dividendYield(Stock[i]))]))
print(" ")
print("GBCE All Share Index: " + str(geometricMean(Stock)))
print(" ")
for i in range(len(result)):
    print(result[i])


