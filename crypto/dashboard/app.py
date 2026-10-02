from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timezone
from src.connectors.binance import ticker,klines,aggregate_trades,order_book,derivatives,DataSourceError
from src.connectors.news import fetch_news
from src.core.features import feature_snapshot
from src.core.signal import build_signal
from src.core.storage import save_snapshot,load_snapshots

st.set_page_config(page_title="Crypto Quant Intelligence",page_icon="₿",layout="wide")
st.markdown("""<style>.block-container{padding-top:1.2rem}.metric-card{background:#111827;padding:16px;border-radius:14px;border:1px solid #263244}.long{color:#23d18b}.short{color:#ff5c77}.neutral{color:#f5c451}</style>""",unsafe_allow_html=True)
st.title("₿ Crypto Quant Intelligence")
st.caption("BTCUSDT 真實市場資料｜可解釋研究訊號｜不自動下單｜非投資建議")

with st.sidebar:
    st.header("控制台")
    interval=st.selectbox("K 線週期",["1m","5m","15m","1h"],index=1)
    topn=st.slider("Order Book 深度",5,100,20,5)
    st.info("按右上角 Rerun 可更新。公開 API 若受所在地網路限制，畫面會顯示錯誤，不會改用假資料。")

try:
    t=ticker(); candles=klines(interval=interval); trades=aggregate_trades(); book=order_book(limit=topn); deriv=derivatives()
    features=feature_snapshot(candles,trades,book,deriv); signal=build_signal(features)
    now=datetime.now(timezone.utc).isoformat(); save_snapshot(now,float(t["lastPrice"]),signal,features)
except DataSourceError as e:
    st.error(f"真實資料來源目前無法存取：{e}")
    st.stop()

cols=st.columns(6)
cols[0].metric("BTCUSDT",f"${float(t['lastPrice']):,.2f}",f"{float(t['priceChangePercent']):.2f}%")
cols[1].metric("Open Interest",f"{deriv['open_interest']:,.0f} BTC")
cols[2].metric("Funding",f"{deriv['funding_rate']*100:.4f}%")
cols[3].metric("Long/Short",f"{deriv['long_short_ratio']:.3f}")
cols[4].metric("Book Imbalance",f"{book['imbalance']:+.3f}")
cols[5].metric("Signal",signal['bias'],f"{signal['score']}/100")

left,right=st.columns([2.2,1])
with left:
    fig=make_subplots(rows=3,cols=1,shared_xaxes=True,vertical_spacing=.03,row_heights=[.58,.20,.22])
    fig.add_trace(go.Candlestick(x=candles.time,open=candles.open,high=candles.high,low=candles.low,close=candles.close,name="BTC"),row=1,col=1)
    colors=['#23d18b' if c>=o else '#ff5c77' for c,o in zip(candles.close,candles.open)]
    fig.add_trace(go.Bar(x=candles.time,y=candles.volume,marker_color=colors,name="Volume"),row=2,col=1)
    fig.add_trace(go.Scatter(x=trades.time,y=trades.cvd,name="Window CVD",line=dict(color="#4da3ff")),row=3,col=1)
    fig.update_layout(height=720,xaxis_rangeslider_visible=False,template="plotly_dark",margin=dict(l=8,r=8,t=25,b=8),legend_orientation="h")
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.subheader(f"{signal['bias']} · {signal['score']}/100")
    st.progress(int(signal['score']))
    st.metric("Confidence",f"{signal['confidence']}/100")
    cdf=pd.DataFrame([{"Factor":k,"Contribution":v} for k,v in signal['contributions'].items()]).sort_values('Contribution')
    cfig=go.Figure(go.Bar(x=cdf.Contribution,y=cdf.Factor,orientation='h',marker_color=['#ff5c77' if x<0 else '#23d18b' for x in cdf.Contribution]))
    cfig.update_layout(height=330,template='plotly_dark',margin=dict(l=5,r=5,t=10,b=5))
    st.plotly_chart(cfig,use_container_width=True)
    st.caption("分數是透明 baseline，用於研究特徵是否具有增量預測能力，不代表獲利保證。")

ncol,hcol=st.columns([1.5,1])
with ncol:
    st.subheader("Central Bank News")
    news=fetch_news()
    if not news: st.warning("Fed RSS 暫時沒有可顯示項目。")
    for item in news:
        st.markdown(f"**[{item['title']}]({item['link']})**  \n{item['source']} · Event baseline {item['event_score']:+d}")
with hcol:
    st.subheader("研究快照")
    hist=load_snapshots(100)
    if hist:
        hdf=pd.DataFrame(hist,columns=['UTC','Price','Score','Bias']).sort_values('UTC')
        st.line_chart(hdf.set_index('UTC')[['Price','Score']])
        st.dataframe(hdf.tail(10),use_container_width=True,hide_index=True)
    st.subheader("資料健康")
    st.success("Binance Spot: OK")
    st.success("Binance Futures: OK")
    st.success("SQLite: OK")
    st.caption(f"最後更新：{now}")
