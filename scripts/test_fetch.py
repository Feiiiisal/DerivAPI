import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import time
from datetime import datetime

from src.fetch_data import get_deriv_api, fetch_candles


async def main():
    now = int(time.time())
    start = now - 86400 * 5
    try:
        candles = await fetch_candles("CRASH500", start, "latest", 86400, 5)
        for candle in candles:
            date = datetime.utcfromtimestamp(candle.get("epoch", 0)).strftime("%Y-%m-%d")
            print(
                f"{date}: O={candle.get('open')} H={candle.get('high')} "
                f"L={candle.get('low')} C={candle.get('close')}"
            )
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())
