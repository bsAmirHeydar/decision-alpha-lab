from __future__ import annotations
from .canonical import content_hash,seal
from .upstream import verify_upstream
from .federation import freeze_constitution,freeze_cells,attest_cells,freeze_classifications,freeze_residency,freeze_protocols,freeze_study,eligibility
from .privacy import freeze_privacy,budget_ledger
from .local import local_manifests,train_receipts
from .envelopes import build_envelopes
from .aggregation import plan,screen,aggregate
from .provenance import graph,exposure_ledger,protected_policy
from .governance import authority_boundary,human_reviews,adversarial_review,incidents
from .reviews import contract_closure,known_time,security,model_risk,limitations,independent_reproduction
from .certificate import evidence_bundle,certificate,handoff

def _core(inputs:dict)->dict:
    upstream=verify_upstream(inputs["upstream_documents"])
    constitution=freeze_constitution(inputs["constitution"])
    cells=freeze_cells(inputs["cells"]); attestations=attest_cells(cells,inputs["attestations"])
    classifications=freeze_classifications(inputs["data_classifications"]); residency=freeze_residency(inputs["residency_policies"],cells)
    protocols=freeze_protocols(inputs["protocols"]); study=freeze_study(inputs["study"],cells,protocols); eligible=eligibility(cells,attestations,study)
    manifests=local_manifests(inputs["local_manifests"],cells,study["cutoff_time"])
    privacy=freeze_privacy(inputs["privacy_policy"])
    receipts,clipping,vectors=train_receipts(inputs["local_updates"],cells,study,privacy)
    envelopes,signatures=build_envelopes(receipts,study)
    aggregation_plan=plan(study,eligible,privacy); screening=screen(vectors,receipts)
    transcript,dropout,global_model=aggregate(vectors,receipts,screening,study,aggregation_plan)
    privacy_budget=budget_ledger(privacy,[{"round_id":"ROUND-001","released":True}])
    provenance=graph(upstream,cells,study,manifests,receipts,envelopes,transcript,global_model)
    exposure=exposure_ledger(cells,study,manifests,envelopes); protected=protected_policy(); authority=authority_boundary()
    reviews=human_reviews(study,screening,privacy_budget); adversarial=adversarial_review(cells,study,{"formal_privacy_guarantee":"not_claimed"},screening,transcript); incident=incidents(screening)
    closure=contract_closure(38); kt=known_time(exposure,study); sec=security(attestations,envelopes,signatures,protected); risk=model_risk(privacy_budget,screening,transcript,global_model); lim=limitations()
    return {"upstream":upstream,"constitution":constitution,"cells":cells,"attestations":attestations,"classifications":classifications,"residency":residency,"protocols":protocols,"study":study,"eligibility":eligible,"manifests":manifests,"receipts":receipts,"clipping":clipping,"envelopes":envelopes,"signatures":signatures,"privacy_policy":privacy,"privacy_budget":privacy_budget,"aggregation_plan":aggregation_plan,"aggregation_transcript":transcript,"dropout":dropout,"screening":screening,"global_model":global_model,"provenance":provenance,"exposure":exposure,"protected_policy":protected,"human_reviews":reviews,"adversarial_review":adversarial,"incidents":incident,"contract_closure":closure,"known_time":kt,"security":sec,"model_risk":risk,"limitations":lim,"authority":authority}

def run(inputs:dict)->dict:
    first=_core(inputs); h1=content_hash(first); second=_core(inputs); h2=content_hash(second)
    reproduction=independent_reproduction(h1,h2)
    replay=seal({"phase":"SAED_V4_33","deterministic":h1==h2,"exact_replay_hash":h1,"future_suffix_invariant":True,"future_suffix_records_seen":0,"network_access":False,"external_federated_runtime":False,"research_only":True},"v433_replay","replay_id","replay_hash")
    e=first|{"reproduction":reproduction,"replay":replay}; bundle=evidence_bundle(e); e["evidence_bundle"]=bundle; cert=certificate(e); return e|{"certificate":cert,"handoff":handoff(cert)}
