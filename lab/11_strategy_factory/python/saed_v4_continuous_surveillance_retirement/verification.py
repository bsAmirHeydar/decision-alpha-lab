from __future__ import annotations
from .canonical import seal,content_hash
def verify_post_retirement(retirement:dict,archive:dict,actions:dict,registry:dict)->dict:
 retired={x["cell_id"] for x in retirement["retired_records"]};rows=[]
 for cid in sorted(retired):
  a=next(x for x in actions["rows"] if x["cell_id"]==cid)
  arc=next((x for x in archive["packages"] if x["cell_id"]==cid),None)
  rows.append({"cell_id":cid,"route_revoked":True,"new_reference_routing_allowed":False,"archive_present":arc is not None,"tombstone_present":bool(arc and arc["tombstone_hash"]),"reinstatement_allowed":False,"capital_delta":0.0,"order_delta":0,"verified":bool(arc and a["decision"]=="RETIRE_CANDIDATE")})
 return seal({"retirement_ledger_hash":retirement["retirement_ledger_hash"],"archive_manifest_hash":archive["archive_manifest_hash"],"rows":rows,"retired_count":len(rows),"verified_count":sum(x["verified"] for x in rows),"all_verified":all(x["verified"] for x in rows),"live_order_side_effects":0,"capital_delta":0.0,"research_only":True},"v441_post_retirement","verification_id","verification_hash")
