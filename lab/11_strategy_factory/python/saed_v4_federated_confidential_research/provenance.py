from __future__ import annotations
from .canonical import content_hash,seal,hash_chain

def graph(upstream,registry,study,manifests,receipts,envelopes,transcript,model):
    nodes=[]
    for kind,obj,id_key,hash_key in [
      ("upstream_receipt",upstream,"receipt_id","receipt_hash"),("cell_registry",registry,"registry_id","registry_hash"),("study",study,"study_spec_id","study_spec_hash"),("local_manifest_registry",manifests,"registry_id","registry_hash"),("local_receipt_registry",receipts,"registry_id","registry_hash"),("envelope_registry",envelopes,"registry_id","registry_hash"),("aggregation_transcript",transcript,"transcript_id","transcript_hash"),("global_model_receipt",model,"receipt_id","receipt_hash")]:
        nodes.append({"node_id":obj[id_key],"node_type":kind,"content_hash":obj[hash_key]})
    edges=[{"from_node":nodes[i]["node_id"],"to_node":nodes[i+1]["node_id"],"relation":"derived_before"} for i in range(len(nodes)-1)]
    return seal({"phase":"SAED_V4_33","nodes":nodes,"edges":edges,"acyclic":True,"complete":True,"research_only":True},"v433_provenance","graph_id","graph_hash")

def exposure_ledger(registry,study,manifests,envelopes):
    events=[]
    for c in registry["cells"]:
        events.append({"cell_id":c["cell_id"],"study_id":study["study_id"],"exposure_type":"study_spec","artifact_hash":study["study_spec_hash"],"protected":False,"raw_data_exposed":False})
        m=next(x for x in manifests["manifests"] if x["cell_id"]==c["cell_id"])
        events.append({"cell_id":c["cell_id"],"study_id":study["study_id"],"exposure_type":"local_manifest","artifact_hash":m["dataset_hash"],"protected":True,"raw_data_exposed":False})
        e=next(x for x in envelopes["envelopes"] if x["cell_id"]==c["cell_id"])
        events.append({"cell_id":c["cell_id"],"study_id":study["study_id"],"exposure_type":"update_commitment","artifact_hash":e["commitment"],"protected":True,"raw_data_exposed":False})
    chained=hash_chain(events,"v433_exposure_event")
    return seal({"phase":"SAED_V4_33","events":chained,"event_count":len(chained),"complete":True,"raw_data_exposure_count":0,"research_only":True},"v433_exposure","ledger_id","ledger_hash")

def protected_policy():
    return seal({"phase":"SAED_V4_33","default":"deny","protected_classes":["local_dataset","local_update","identity_material","credentials","hidden_evaluation"],"permitted_cross_cell_artifacts":["aggregate_update","commitment","content_hash","privacy_receipt","schema_hash","signed_handoff_reference"],"raw_data_broadcast":False,"credential_distribution":False,"hidden_evaluation_broadcast":False,"human_exception_required":True,"research_only":True},"v433_protected_policy","policy_id","policy_hash")
