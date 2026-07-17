from __future__ import annotations
import copy,json
from _common import EX
from saed_v4_sovereign_distributed_compute import run
x=json.loads((EX/"GOLDEN_INPUT.JSON").read_text());a=run(x);b=run(copy.deepcopy(x));assert a==b;assert a["replay"]["deterministic"] and a["determinism"]["exact_match"]
print("V4-34 deterministic replay passed")
