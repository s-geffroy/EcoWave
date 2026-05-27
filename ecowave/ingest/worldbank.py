from __future__ import annotations

import pandas as pd
import requests


def fetch_worldbank_indicator(country: str, indicator: str, api_base: str) -> pd.DataFrame:
    url = f"{api_base}/country/{country}/indicator/{indicator}"
    params = {"format": "json", "per_page": 20000}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    rows = data[1] if isinstance(data, list) and len(data) > 1 else []
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=["date", "value"])
    return df[["date", "value"]]
