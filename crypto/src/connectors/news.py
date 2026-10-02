import feedparser
FEEDS={"Federal Reserve":"https://www.federalreserve.gov/feeds/press_all.xml"}
POS=("approval","growth","support","easing","cut","liquidity")
NEG=("sanction","war","attack","inflation","tightening","risk","enforcement")
def fetch_news(limit=12):
    items=[]
    for source,url in FEEDS.items():
        d=feedparser.parse(url)
        for e in d.entries[:limit]:
            title=e.get("title",""); low=title.lower()
            score=sum(w in low for w in POS)-sum(w in low for w in NEG)
            items.append({"source":source,"title":title,"link":e.get("link",""),"published":e.get("published",""),"event_score":max(-1,min(1,score))})
    return items[:limit]
