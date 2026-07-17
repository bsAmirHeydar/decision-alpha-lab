from __future__ import annotations
import json
from _common import AR,EX,MAP
from saed_v4_federated_confidential_research.service import run
inputs=json.loads((EX/"FULL_REFERENCE_INPUT.JSON").read_text(encoding="utf-8")); result=run(inputs); AR.mkdir(parents=True,exist_ok=True)
for key,name in MAP.items(): (AR/name).write_text(json.dumps(result[key],indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(f"V4-33 golden reproduction complete: {len(MAP)} artifacts")
