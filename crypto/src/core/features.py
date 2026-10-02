import numpy as np

def feature_snapshot(candles,trades,book,deriv):
    ret5=(candles.close.iloc[-1]/candles.close.iloc[-2]-1) if len(candles)>1 else 0
    ret20=(candles.close.iloc[-1]/candles.close.iloc[-20]-1) if len(candles)>=20 else 0
    rv=float(candles.close.pct_change().tail(30).std() or 0)
    cvd=float(trades.cvd.iloc[-1]) if trades is not None and not trades.empty else 0
    total=float(trades.qty.sum()) if trades is not None and not trades.empty else 0
    cvd_norm=cvd/total if total else 0
    return {"return_1bar":ret5,"momentum_20":ret20,"volatility":rv,"cvd_norm":cvd_norm,"orderbook_imbalance":book["imbalance"],"open_interest":deriv["open_interest"],"funding_rate":deriv["funding_rate"],"long_short_ratio":deriv.get("long_short_ratio") or 1.0}
