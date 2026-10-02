# DerivAPI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

Download historical candle (OHLC) data for Deriv synthetic indices such as
`CRASH300` and `CRASH500` through the Deriv WebSocket API, then clean it into
a tidy daily time series ready for analysis and modelling.

## What it does

- **Fetches candles** from the Deriv API with an authorised, reusable client
  (`src/fetch_data.py`).
- **Pages through history automatically**: `fetch_all_candles` requests
  1,000 candles at a time, walking backwards from the latest bar until
  everything since your chosen start date has been collected.
- **Cleans the data**: `src/processing.py` reindexes the raw series onto
  business days and forward-fills gaps.
- **Keeps credentials out of the code**: the app ID and token are read from a
  `.env` file.

## Project layout

```
src/
  fetch_data.py    Deriv API client, fetch_candles, fetch_all_candles
  processing.py    Clean raw crash500 candles into a business-day series
scripts/
  download_all_candles.py   Download CRASH300 daily candles since 2022-01-01
  test_fetch.py             Quick check: fetch the last 5 daily CRASH500 candles
  setup_env.sh              Create a virtual environment and install dependencies
data/               Raw and processed CSV files (created when you run the scripts)
requirements.txt
.env.example
```

`notebooks/` and `tests/` are placeholders: there are no notebooks or automated
tests yet.

## Setup

```bash
# 1. Create a virtual environment and install dependencies
bash scripts/setup_env.sh          # or: python -m venv venv && pip install -r requirements.txt

# 2. Add your Deriv credentials
cp .env.example .env               # then edit .env with your own values
```

Never commit `.env`; it is listed in `.gitignore`.

## Usage

Run these from the repository root:

```bash
# Check that your credentials work (prints the last 5 daily candles)
python scripts/test_fetch.py

# Download all daily CRASH300 candles since 2022-01-01 -> data/raw/crash300_daily.csv
python -m scripts.download_all_candles

# Clean data/raw/crash500_daily.csv -> data/processed/crash500_daily_clean.csv
python -m src.processing
```

Or use the client from your own code:

```python
import asyncio, time
from src.fetch_data import fetch_all_candles

start = int(time.time()) - 365 * 24 * 3600
candles = asyncio.run(fetch_all_candles("CRASH500", start, 86400))  # daily candles
print(len(candles), candles[0])
```

## Disclaimer

This project is for research and education. It is not financial advice.

## License

[MIT](LICENSE)
