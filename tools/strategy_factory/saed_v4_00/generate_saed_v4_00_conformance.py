#!/usr/bin/env python3
from __future__ import annotations
import json,os,sys,yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_constitution.canonical import content_hash
from saed_v4_constitution.conformance import run_vector
from saed_v4_constitution.policy import ConstitutionKernel
E=ROOT/'lab/11_strategy_factory/examples/saed_v4_00'
constitution=yaml.safe_load((E/'research_constitution.yaml').read_text(encoding='utf-8'))
vectors=json.loads((E/'constitutional_conformance_vectors.json').read_text(encoding='utf-8'))
kernel=ConstitutionKernel(content_hash(constitution))
results=[run_vector(kernel,v) for v in vectors['vectors']]
out={'status':'pass' if all(x['matches_expected'] for x in results) else 'fail','passed':sum(x['matches_expected'] for x in results),'total':len(results),'results':results}
path=ROOT/'lab/11_strategy_factory/artifacts/SAED_V4_00_CONFORMANCE_RESULTS.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'output':str(path.relative_to(ROOT)),**{k:out[k] for k in ('status','passed','total')}},indent=2))
raise SystemExit(0 if out['status']=='pass' else 1)
