def _clip(x,lo,hi): return max(lo,min(hi,x))
def build_signal(f):
    contributions={
      "Momentum": _clip(f["momentum_20"]*500,-18,18),
      "CVD": _clip(f["cvd_norm"]*30,-18,18),
      "Order Book": _clip(f["orderbook_imbalance"]*15,-12,12),
      "Funding Risk": -_clip(f["funding_rate"]*100000,-8,8),
      "Long/Short Crowding": -_clip((f["long_short_ratio"]-1)*8,-8,8),
      "Volatility Risk": -_clip(f["volatility"]*1000,0,8),
    }
    raw=sum(contributions.values()); score=_clip(50+raw,0,100)
    bias="LONG BIAS" if score>=60 else "SHORT BIAS" if score<=40 else "NEUTRAL"
    agreement=sum(1 for v in contributions.values() if (v>0)==(raw>0))/len(contributions) if raw else .5
    confidence=_clip(45+agreement*40-min(15,f["volatility"]*1500),0,100)
    return {"bias":bias,"score":round(score,1),"confidence":round(confidence,1),"contributions":{k:round(v,1) for k,v in contributions.items()}}
