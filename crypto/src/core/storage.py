import sqlite3, json
from pathlib import Path
DB=Path(__file__).resolve().parents[2]/"data"/"crypto.db"
def init_db():
    DB.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB) as c:
        c.execute("CREATE TABLE IF NOT EXISTS snapshots (ts TEXT PRIMARY KEY, price REAL, score REAL, bias TEXT, payload TEXT)")
def save_snapshot(ts,price,signal,features):
    init_db()
    with sqlite3.connect(DB) as c:
        c.execute("INSERT OR REPLACE INTO snapshots VALUES (?,?,?,?,?)",(ts,float(price),signal["score"],signal["bias"],json.dumps(features)))
def load_snapshots(limit=500):
    init_db()
    with sqlite3.connect(DB) as c:
        return c.execute("SELECT ts,price,score,bias FROM snapshots ORDER BY ts DESC LIMIT ?",(limit,)).fetchall()
