from __future__ import annotations
from .canonical import content_hash,stable_id

def decide(intake,disclosure):
    reasons=[]
    if not intake.license_permitted: reasons.append('license_not_permitted')
    if not intake.architecture_disclosed: reasons.append('architecture_not_disclosed')
    if not intake.local_execution_only or not intake.remote_inference_forbidden: reasons.append('remote_dependency_forbidden')
    if disclosure.intake_id!=intake.intake_id: reasons.append('disclosure_binding_mismatch')
    if not disclosure.contamination_reviewed: reasons.append('contamination_review_missing')
    if intake.overlap_risk in {'high','unknown'} and not intake.synthetic_reference_adapter: reasons.append('unbounded_overlap_risk')
    if intake.source_kind!='reference_emulation' and not intake.exact_corpus_disclosed: reasons.append('opaque_external_corpus')
    if not intake.enabled: decision='reject'; reasons.append('disabled')
    elif reasons: decision='quarantine'
    else: decision='admit_reference'
    doc={'phase':'SAED_V4_14','intake_id':intake.intake_id,'family':intake.family,'decision':decision,'reasons':sorted(set(reasons)),'synthetic_reference_adapter':intake.synthetic_reference_adapter,'external_weights_loaded':False,'production_eligible':False}
    doc['decision_hash']=content_hash(doc);doc['decision_id']=stable_id('fmintake',doc);return doc

def decide_all(intakes,disclosures):
    by={x.intake_id:x for x in disclosures}; return [decide(i,by[i.intake_id]) for i in intakes]
