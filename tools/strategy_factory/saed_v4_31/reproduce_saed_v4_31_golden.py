from __future__ import annotations
import json
from _common import AR,MAP,reference_result
result=reference_result(); AR.mkdir(parents=True,exist_ok=True)
for key,name in MAP.items(): (AR/name).write_text(json.dumps(result[key],indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(f"V4-31 golden reproduction complete: {len(MAP)} exact artifacts")
