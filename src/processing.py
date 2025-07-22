"""Utility to clean crash500 candle data."""

from __future__ import annotations

import pandas as pd

RAW_PATH = "data/raw/crash500_daily.csv"
CLEAN_PATH = "data/processed/crash500_daily_clean.csv"


def process_crash500() -> None:
    """Load raw data, reindex on business days, and forward fill."""
    df = pd.read_csv(RAW_PATH)
    df["epoch"] = pd.to_datetime(df["epoch"], unit="s")
    df.set_index("epoch", inplace=True)
    df.sort_index(inplace=True)

    idx = pd.date_range(df.index.min(), df.index.max(), freq="B")
    df = df.reindex(idx)
    df.ffill(inplace=True)

    df.to_csv(CLEAN_PATH)


if __name__ == "__main__":
    process_crash500()
