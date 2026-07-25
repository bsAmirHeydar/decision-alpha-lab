from __future__ import annotations
from .canonical import content_hash,stable_id

def create_assignments(registry:dict,package:dict,protocol:dict)->tuple[dict,dict]:
    assignments=[]; receipts=[]
    for index,lab in enumerate(registry["labs"],1):
        blind_code=stable_id("blind",{"package":package["package_id"],"lab":lab["lab_id"]},16)
        assignment={"assignment_index":index,"lab_id":lab["lab_id"],"package_id":package["package_id"],"protocol_id":protocol["protocol_id"],"blind_code":blind_code,"candidate_identity_visible":False,"hidden_labels_visible":False,"raw_protected_rows_visible":False,"opened":False,"maximum_runs":1,"research_only":True}
        assignment["assignment_id"]=stable_id("v430_assignment",assignment); assignment["assignment_hash"]=content_hash(assignment); assignments.append(assignment)
        receipt={"assignment_id":assignment["assignment_id"],"sender_role":"replication_custodian","receiver_lab_id":lab["lab_id"],"transport_mode":"sealed_local_reference","package_hash":package["package_hash"],"network_egress":False,"payload_mutated":False,"delivered":True}
        receipt["receipt_id"]=stable_id("v430_exchange",receipt); receipt["receipt_hash"]=content_hash(receipt); receipts.append(receipt)
    bundle={"phase":"SAED_V4_30","package_id":package["package_id"],"assignments":assignments,"assignment_count":len(assignments),"one_assignment_per_lab":True,"research_only":True}
    bundle["bundle_id"]=stable_id("v430_assignments",bundle); bundle["bundle_hash"]=content_hash(bundle)
    exchange={"phase":"SAED_V4_30","receipts":receipts,"receipt_count":len(receipts),"all_delivered":True,"raw_data_transfers":0,"round_trips":0,"research_only":True}
    exchange["exchange_id"]=stable_id("v430_exchange_manifest",exchange); exchange["exchange_hash"]=content_hash(exchange)
    return bundle,exchange
