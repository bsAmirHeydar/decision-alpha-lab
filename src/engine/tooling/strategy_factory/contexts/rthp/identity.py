from __future__ import annotations
import hashlib,json
def stable_event_id(request:dict)->str:
 fields=["context_id","family","pair_id","cycle_definition_version","active_cycle_id","reference_cycle_id","level_side","confirmation_close_time"]
 material={k:request.get(k) for k in fields}; material["hunter_symbol"]=request.get("hunter_symbol"); material["protected_symbol"]=request.get("protected_symbol"); material["first_touch_time"]=request.get("first_touch_time")
 raw=json.dumps(material,sort_keys=True,separators=(",",":")).encode();return "RTHPEVT_"+hashlib.sha256(raw).hexdigest()[:32].upper()
