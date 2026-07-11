from __future__ import annotations
import csv,json,hashlib
from pathlib import Path
from dataclasses import asdict

def write_json(path, obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,sort_keys=True,default=str)+"\n",encoding="utf-8")

def write_selected_csv(path,items):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(["rank","public_id","score","status","unique_events","filled","fill_rate","expectancy_r","profit_factor","max_drawdown_r","best_trade_share","summary_hash"])
        for i,s in enumerate(items,1):w.writerow([i,s.public_id,s.objective_score,s.status.name,s.metrics.unique_event_count,s.metrics.filled_count,s.metrics.fill_rate,s.metrics.expectancy_r,s.metrics.profit_factor,s.metrics.maximum_drawdown_r,s.metrics.best_trade_share,s.summary_hash])

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):h.update(chunk)
    return h.hexdigest()
