"""Helpers to connect to Deriv API and retrieve candle data."""

from __future__ import annotations

import os
from typing import Dict, List, Union

from deriv_api import DerivAPI, ResponseError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DERIV_APP_ID = os.getenv("DERIV_APP_ID")
DERIV_TOKEN = os.getenv("DERIV_TOKEN")

# Singleton API instance
_api_client: DerivAPI | None = None

async def get_deriv_api() -> DerivAPI:
    """Return an authorized :class:`DerivAPI` client.

    The client is created on first call using ``DERIV_APP_ID`` and
    ``DERIV_TOKEN`` values loaded from ``.env``. Subsequent calls return the
    same instance.
    """
    global _api_client

    if _api_client is None:
        if not DERIV_APP_ID or not DERIV_TOKEN:
            raise RuntimeError(
                "DERIV_APP_ID and DERIV_TOKEN must be set in the .env file"
            )

        # Initialize API and authorize session
        _api_client = DerivAPI(app_id=DERIV_APP_ID)
        await _api_client.authorize(DERIV_TOKEN)

    return _api_client


async def fetch_candles(
    symbol: str,
    start: int,
    end: Union[int, str],
    granularity: int,
    count: int,
) -> List[Dict]:
    """Fetch candle data for ``symbol`` between ``start`` and ``end``.

    Parameters
    ----------
    symbol : str
        Market symbol to query.
    start : int
        Epoch timestamp marking the start of the range.
    end : Union[int, str]
        Epoch timestamp marking the end of the range or ``"latest"``.
    granularity : int
        Time dimension for each candle in seconds.
    count : int
        Maximum number of candles to fetch.

    Returns
    -------
    List[Dict]
        List of candle dictionaries returned by the Deriv API.

    Raises
    ------
    ResponseError
        If the API response contains an error.
    """
    api = await get_deriv_api()

    response = await api.ticks_history(
        {
            "ticks_history": symbol,
            "start": start,
            "end": end,
            "granularity": granularity,
            "count": count,
            "style": "candles",
        }
    )

    # Raise an exception if the response contains an error
    if isinstance(response, dict) and response.get("error"):
        raise ResponseError(response)

    candles = response.get("candles", [])
    return list(candles)


async def fetch_all_candles(
    symbol: str,
    start: int,
    granularity: int,
    page_size: int = 1000,
) -> List[Dict]:
    """Fetch all available candles for ``symbol`` starting at ``start``.

    The function pages through results ``page_size`` bars at a time until no
    more data is available, returning a list of candles sorted in ascending
    order by ``epoch``.
    """

    all_candles: List[Dict] = []
    end: Union[int, str] = "latest"

    while True:
        batch = await fetch_candles(symbol, start, end, granularity, page_size)
        if not batch:
            break

        batch_sorted = sorted(batch, key=lambda c: c["epoch"])
        all_candles = batch_sorted + all_candles if all_candles else batch_sorted

        if len(batch) < page_size:
            break

        oldest = batch_sorted[0]["epoch"]
        end = oldest - granularity

    return all_candles


if __name__ == "__main__":
    import asyncio
    import time

    start = int(time.time()) - 365 * 24 * 3600
    candles = asyncio.run(fetch_all_candles("CRASH500", start, 86400))
    print(f"Fetched {len(candles)} daily candles")
    print("First:", candles[0])
    print("Last: ", candles[-1])

