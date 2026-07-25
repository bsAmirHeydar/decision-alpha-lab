from __future__ import annotations
import json
from pathlib import Path
from .detector import evaluate_divergence
def validate_fixtures(root:Path)->dict:
 failed=[];count=0
 for p in sorted((root/"fixtures/golden").glob("*.json")):
  count+=1;case=json.loads(p.read_text());actual=evaluate_divergence(case["input"]);exp=case["expected"]
  for k,v in exp.items():
   if actual.get(k)!=v:failed.append({"case":case["input"]["case_id"],"field":k,"expected":v,"actual":actual.get(k)})
 return {"passed":not failed,"count":count,"failures":failed}
