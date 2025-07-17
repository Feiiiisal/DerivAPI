import asyncio
import time
import os
import csv

from src.fetch_data import fetch_all_candles


start = int(time.mktime(time.strptime("2022-01-01", "%Y-%m-%d")))

candles = asyncio.run(fetch_all_candles("CRASH300", start, 86400))

os.makedirs("data/raw", exist_ok=True)

csv_path = os.path.join("data", "raw", "crash300_daily.csv")
with open(csv_path, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["epoch", "open", "high", "low", "close"])
    writer.writeheader()
    for candle in candles:
        writer.writerow({
            "epoch": candle.get("epoch"),
            "open": candle.get("open"),
            "high": candle.get("high"),
            "low": candle.get("low"),
            "close": candle.get("close"),
        })

print(f"Saved {len(candles)} candles to {csv_path}")
