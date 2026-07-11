from __future__ import annotations
import argparse,json
from pathlib import Path
from .models import OutcomeView,ObjectiveConfig,PassSummary
from .accumulator import ResearchAccumulator
from .objective import evaluate_objective

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument("outcomes");p.add_argument("--output",default="research_summary.json");a=p.parse_args(argv)
    rows=json.loads(Path(a.outcomes).read_text());acc=ResearchAccumulator()
    for row in rows:acc.observe(OutcomeView(**row))
    m=acc.snapshot();r=evaluate_objective(m,ObjectiveConfig(minimum_unique_events=1,minimum_filled_outcomes=1))
    Path(a.output).write_text(json.dumps({"metrics":m.__dict__ if hasattr(m,"__dict__") else {k:getattr(m,k) for k in m.__slots__},"objective":{"score":r.score,"status":r.status.name,"reason":r.reason}},indent=2,default=str)+"\n")
    return 0
if __name__=="__main__":raise SystemExit(main())
