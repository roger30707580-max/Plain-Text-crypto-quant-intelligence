# Crypto Quant Intelligence Desktop Web MVP

這是一個可在電腦瀏覽器開啟的 Streamlit 研究儀表板。使用真實公開市場資料，不會自動下單。

## 已完成
- BTCUSDT 即時價格、24h 漲跌
- 1m/5m/15m/1h K 線與成交量
- 近期 aggregate trades 推算 CVD
- Spot order book imbalance
- Futures open interest、funding、global long/short ratio
- Fed 官方 RSS
- 透明 LONG / NEUTRAL / SHORT 研究訊號與貢獻拆解
- SQLite 快照保存
- 簡易歷史 baseline backtest
- API 健康狀態與資料缺失降級

## 限制
- CVD 是用 API 最近最多 1000 筆 aggregate trades 計算的視窗 CVD，不是完整歷史 CVD。長期累積需執行 collector。
- 公開 API 可能受地區、網路或交易所服務條款限制。
- 新聞規則分數只是 baseline，不代表因果影響。
- 所有訊號只供研究，不構成投資建議。

## Windows 啟動
解壓縮後，雙擊 `run_windows.bat`。完成安裝後瀏覽器會開啟。

## 手動啟動
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## 測試
```bash
pytest -q
```
