from __future__ import annotations
import csv, json
from pathlib import Path
from .models import FoldObservation, ValidationPlan, StressScenario
from .enums import FoldRole, SplitMethod, StressKind

def read_fold_observations_csv(path: str | Path) -> tuple[FoldObservation,...]:
    rows=[]
    with Path(path).open(newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(FoldObservation(
              observation_id=r["observation_id"],trial_id=r["trial_id"],
              parameter_hash=r["parameter_hash"],fold_id=r["fold_id"],
              role=FoldRole(int(r["role"])),event_id=r["event_id"],
              cluster_id=r["cluster_id"],outcome_id=r["outcome_id"],
              known_time_utc_msc=int(r["known_time_utc_msc"]),
              resolved_time_utc_msc=int(r["resolved_time_utc_msc"]),
              net_r=float(r["net_r"]),gross_r=float(r["gross_r"]),
              cost_r=float(r["cost_r"]),ambiguous=r.get("ambiguous","false").lower()=="true",
              observation_hash=r.get("observation_hash","") ))
    return tuple(rows)

def read_validation_plan(path: str | Path) -> ValidationPlan:
    d=json.loads(Path(path).read_text(encoding="utf-8")); d.pop("schema",None)
    d["method"]=SplitMethod(d["method"]); return ValidationPlan(**d)

def read_stress_scenarios(path: str | Path) -> tuple[StressScenario,...]:
    data=json.loads(Path(path).read_text(encoding="utf-8")); data=data.get("scenarios",data)
    result=[]
    for d in data:
        d=dict(d); d.pop("schema",None); d["kind"]=StressKind(d["kind"])
        result.append(StressScenario(**d))
    return tuple(result)
