from __future__ import annotations
import json
from _common import AR
for n in ["GOLDEN_HUMAN_REVIEW_CHECKPOINTS.JSON","GOLDEN_SECURITY_REVIEW.JSON","GOLDEN_MODEL_RISK_REVIEW.JSON","GOLDEN_FAULT_TOLERANCE_REVIEW.JSON","GOLDEN_UCEE_COMPATIBILITY.JSON"]: assert json.loads((AR/n).read_text())["research_only"] is True
assert json.loads((AR/"GOLDEN_UCEE_COMPATIBILITY.JSON").read_text())["central_engine_mutations"]==0
print("V4-34 governance validation passed")
