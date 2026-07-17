from __future__ import annotations
import json
from _common import AR
b=json.loads((AR/"GOLDEN_AUTHORITY_BOUNDARY.JSON").read_text()); c=json.loads((AR/"GOLDEN_SOVEREIGN_DISTRIBUTED_COMPUTE_CERTIFICATE.JSON").read_text())
for k in ["may_export_raw_data","may_mutate_ucee","may_select_treatment","may_allocate_risk","may_compile_live_runtime","may_send_order","promotion_authority","production_authorization","live_trading_authority"]: assert b[k] is False
assert c["promotion_authority"] is False and c["execution_authority"] is False and c["production_authorization"] is False
print("V4-34 authority boundaries passed")
