from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import csv, json
from .models import StatisticalSample

def read_samples_csv(path: str|Path) -> list[StatisticalSample]:
    rows=[]
    with Path(path).open(newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            rows.append(StatisticalSample(
                sample_id=r['sample_id'],outcome_id=r['outcome_id'],candidate_id=r['candidate_id'],
                event_id=r['event_id'],cluster_id=r['cluster_id'],strategy_id=r['strategy_id'],symbol=r['symbol'],
                direction=r['direction'],session_id=r['session_id'],year=int(r['year']),month=int(r['month']),
                weekday=int(r['weekday']),stratum_key=r['stratum_key'],filled=r['filled'].lower()=='true',
                ambiguous=r['ambiguous'].lower()=='true',net_r=float(r['net_r']),mfe_r=float(r['mfe_r']),
                mae_r=float(r['mae_r']),holding_seconds=float(r['holding_seconds']),weight=float(r.get('weight',1)),
                known_time_utc_msc=int(r.get('known_time_utc_msc',0))))
    return rows

def write_json(path: str|Path, value) -> None:
    Path(path).write_text(json.dumps(value,indent=2,sort_keys=True,default=lambda x:asdict(x)),encoding='utf-8')
