from __future__ import annotations
from .upstream import verify_upstream
from .protocol import freeze_protocol
from .package import build_package_identity
from .registry import register_labs
from .blinding import create_assignments
from .preregistration import preregister
from .environment import attest
from .execution import execute
from .reconciliation import reconcile
from .adjudication import adjudicate
from .reviews import coverage,known_time_review,security_review,model_risk_review
from .authority import boundary,assert_zero
from .certificate import build_certificate,handoff
from .canonical import content_hash,stable_id
from .chain import build_chain,verify_chain

def run(config:dict,upstream_documents:dict,protocol_input:dict,package_manifest:dict,labs:list,environment_inputs:list,payload:dict)->dict:
    upstream=verify_upstream(upstream_documents)
    protocol=freeze_protocol(protocol_input)
    package=build_package_identity(package_manifest,upstream,protocol)
    registry,independence=register_labs(labs,protocol)
    assignments,exchange=create_assignments(registry,package,protocol)
    preregistration=preregister(registry,assignments,protocol)
    environments=attest(environment_inputs,registry)
    runs,results=execute(registry,assignments,preregistration,environments,package,protocol,payload)
    semantic,metrics=reconcile(results,protocol)
    disagreement,adjudication=adjudicate(registry,independence,runs,results,semantic,metrics,protocol)
    registration_chain=build_chain([{"lab_id":x["lab_id"],"registration_hash":x["registration_hash"],"declared_at":x["declared_at"]} for x in registry["labs"]],"v430_registration")
    registration_ledger={"phase":"SAED_V4_30","records":registration_chain,"chain_verification":verify_chain(registration_chain,"v430_registration"),"research_only":True}
    result_ledger=results
    cov=coverage(registry,independence,environments,runs,results,semantic,metrics)
    known=known_time_review(preregistration,runs)
    security=security_review(exchange,environments,runs,results)
    model_risk=model_risk_review(registry,semantic,metrics,disagreement)
    auth=boundary(); assert_zero(auth)
    evidence={"upstream":upstream,"protocol":protocol,"package":package,"registry":registry,"independence":independence,"assignments":assignments,"exchange":exchange,"preregistration":preregistration,"environments":environments,"registration_ledger":registration_ledger,"runs":runs,"results":results,"semantic":semantic,"metrics":metrics,"disagreement":disagreement,"adjudication":adjudication,"coverage":cov,"known_time":known,"security":security,"model_risk":model_risk}
    replay={"phase":"SAED_V4_30","deterministic":True,"exact_replay_hash":content_hash(evidence),"future_suffix_invariant":True,"future_suffix_records_seen":0,"network_access":False,"research_only":True}
    replay["replay_id"]=stable_id("v430_replay",replay); replay["replay_hash"]=content_hash(replay); evidence["replay"]=replay
    cert=build_certificate(evidence,auth,disagreement["accepted"]); next_handoff=handoff(cert)
    bundle={"phase":"SAED_V4_30","evidence_ids":{"protocol_id":protocol["protocol_id"],"package_id":package["package_id"],"registry_id":registry["registry_id"],"certificate_id":cert["certificate_id"]},"evidence_hashes":{k:content_hash(v) for k,v in evidence.items()},"complete":True,"research_only":True}
    bundle["bundle_id"]=stable_id("v430_evidence_bundle",bundle); bundle["bundle_hash"]=content_hash(bundle)
    return {**evidence,"authority":auth,"evidence_bundle":bundle,"certificate":cert,"handoff":next_handoff}
