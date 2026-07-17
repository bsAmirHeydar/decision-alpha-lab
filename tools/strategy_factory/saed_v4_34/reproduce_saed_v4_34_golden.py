from __future__ import annotations
import json
from _common import ROOT,AR,EX,MAP
from saed_v4_sovereign_distributed_compute import run
r=run(json.loads((EX/"GOLDEN_INPUT.JSON").read_text()))
for k,n in MAP.items():
    expected=json.loads((AR/n).read_text()); assert r[k]==expected,k
print(f"V4-34 golden reproduction passed: {len(MAP)} artifacts")
