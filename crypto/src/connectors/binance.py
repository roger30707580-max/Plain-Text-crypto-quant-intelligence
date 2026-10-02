from __future__ import annotations
import requests
import pandas as pd

SPOT = "https://data-api.binance.vision"
FUTURES = "https://fapi.binance.com"

class DataSourceError(RuntimeError): pass

def _get(base, path, params=None):
    try:
        r=requests.get(base+path,params=params,timeout=12)
        r.raise_for_status()
        data=r.json()
        if isinstance(data,dict) and "code" in data and int(data.get("code",0))<0:
            raise DataSourceError(str(data))
        return data
    except Exception as e:
        raise DataSourceError(f"Binance request failed: {e}") from e

def ticker(symbol="BTCUSDT"):
    return _get(SPOT,"/api/v3/ticker/24hr",{"symbol":symbol})

def klines(symbol="BTCUSDT", interval="5m", limit=300):
    raw=_get(SPOT,"/api/v3/klines",{"symbol":symbol,"interval":interval,"limit":limit})
    cols=["open_time","open","high","low","close","volume","close_time","quote_volume","trades","taker_buy_volume","taker_buy_quote","ignore"]
    df=pd.DataFrame(raw,columns=cols)
    for c in ["open","high","low","close","volume","quote_volume","taker_buy_volume"]: df[c]=pd.to_numeric(df[c])
    df["time"]=pd.to_datetime(df["open_time"],unit="ms",utc=True)
    return df

def aggregate_trades(symbol="BTCUSDT", limit=1000):
    raw=_get(SPOT,"/api/v3/aggTrades",{"symbol":symbol,"limit":limit})
    df=pd.DataFrame(raw)
    if df.empty: return df
    df["time"]=pd.to_datetime(df["T"],unit="ms",utc=True)
    df["price"]=pd.to_numeric(df["p"]); df["qty"]=pd.to_numeric(df["q"])
    df["signed_qty"]=df.apply(lambda r: -r["qty"] if bool(r["m"]) else r["qty"],axis=1)
    df["cvd"]=df["signed_qty"].cumsum()
    return df

def order_book(symbol="BTCUSDT", limit=20):
    d=_get(SPOT,"/api/v3/depth",{"symbol":symbol,"limit":limit})
    bid=sum(float(x[1]) for x in d["bids"]); ask=sum(float(x[1]) for x in d["asks"])
    imbalance=(bid-ask)/(bid+ask) if bid+ask else 0.0
    return {"bid_volume":bid,"ask_volume":ask,"imbalance":imbalance,"last_update_id":d["lastUpdateId"]}

def derivatives(symbol="BTCUSDT"):
    oi=_get(FUTURES,"/fapi/v1/openInterest",{"symbol":symbol})
    premium=_get(FUTURES,"/fapi/v1/premiumIndex",{"symbol":symbol})
    ratio=_get(FUTURES,"/futures/data/globalLongShortAccountRatio",{"symbol":symbol,"period":"5m","limit":2})
    return {"open_interest":float(oi["openInterest"]),"funding_rate":float(premium["lastFundingRate"]),"mark_price":float(premium["markPrice"]),"long_short_ratio":float(ratio[-1]["longShortRatio"]) if ratio else None}
