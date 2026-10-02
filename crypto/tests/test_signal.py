from src.core.signal import build_signal
def test_signal_bounds():
    f={"momentum_20":.01,"cvd_norm":.2,"orderbook_imbalance":.2,"funding_rate":.0001,"long_short_ratio":1.1,"volatility":.002}
    s=build_signal(f)
    assert 0<=s["score"]<=100
    assert s["bias"] in {"LONG BIAS","NEUTRAL","SHORT BIAS"}
