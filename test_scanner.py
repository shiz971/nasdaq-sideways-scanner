import yfinance as yf
import pandas_ta as ta
import pandas as pd

ticker = "AAPL"

print("Downloading data for", ticker)
df = yf.download(ticker, period="30d")

macd = ta.macd(df["Close"])
df = pd.concat([df, macd], axis=1)

df["price_range_pct"] = (df["High"] - df["Low"]) / ((df["High"] + df["Low"]) / 2)

recent = df.tail(3)

print("\nLast 3 trading days:")
print(recent[[
    "Close",
    "price_range_pct",
    "MACDh_12_26_9",
    "MACD_12_26_9",
    "MACDs_12_26_9"
]])

print("\nSideways checks:")
print("Price range <= 1.5%:", recent["price_range_pct"].max() <= 0.015)
print("Low momentum (MACD hist):", recent["MACDh_12_26_9"].abs().max() <= 0.05)

macd_diff = recent["MACD_12_26_9"] - recent["MACDs_12_26_9"]
print("No MACD crossover:", macd_diff.apply(lambda x: x > 0).nunique() == 1)
