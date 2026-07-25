from pathlib import Path
from .io import load_json
from .canonical import digest_object
def verify_handoff(path:Path)->dict:
 d=load_json(path);return {"passed":d.get("handoff_type")=="LCM10B_TO_LCM10C" and d.get("handoff_digest")==digest_object(d,"handoff_digest") and not d.get("live_order_authority_created") and not d.get("capital_authority_created"),"handoff":d}
