from __future__ import annotations
from collections import Counter
from .canonical import content_hash, stable_id, merkle_root
from .models import CorpusRecord
from .validation import validate_records, validate_upstream_manifest, validate_v4_10_handoff
from .errors import ContractError, LeakageError

ALLOWED_ROLES={"development","training","validation"}

def build_corpus_manifest(records:list[dict], upstream_manifest:dict, handoff:dict)->dict:
    validate_upstream_manifest(upstream_manifest)
    validate_v4_10_handoff(handoff,upstream_manifest)
    objs=validate_records(records)
    role_counts=Counter(x.evidence_role for x in objs)
    if set(role_counts)-ALLOWED_ROLES: raise ContractError('unsupported corpus role')
    source_hashes=sorted({h for x in objs for h in x.source_hashes})
    record_hashes=[content_hash(r) for r in sorted(records,key=lambda x:x['record_id'])]
    payload={
      "phase":"SAED_V4_11","exact_version":"1.0.0","upstream_phase":"SAED_V4_10",
      "upstream_handoff_id":handoff['handoff_id'],"upstream_handoff_hash":handoff['handoff_hash'],
      "upstream_corpus_manifest_id":upstream_manifest['manifest_id'],"upstream_corpus_manifest_hash":upstream_manifest['manifest_hash'],
      "self_supervised_only":True,"future_suffix_allowed":False,"outcome_inputs_allowed":False,
      "record_count":len(records),"role_counts":dict(sorted(role_counts.items())),
      "root_context_count":len({x.root_context_id for x in objs}),"domain_count":len({x.domain_id for x in objs}),
      "record_merkle_root":merkle_root(record_hashes),"source_hashes":source_hashes,
      "allowed_artifact_classes":["multimodal_view_package","semantic_temporal_hypergraph","action_lattice_descriptors"],
      "prohibited_artifact_classes":list(upstream_manifest['prohibited_input_artifact_classes']),
      "synthetic_reference_only":all(x.synthetic for x in objs),
      "limitations":["Synthetic reference corpus only.","No protected, prospective, shadow or live evidence.","No outcome or execution artifact is an encoder input."]
    }
    payload['manifest_id']=stable_id('v411corpus',payload)
    payload['manifest_hash']=content_hash(payload)
    return payload

def corpus_membership(records:list[dict])->dict:
    objs=validate_records(records)
    entries=[]
    for x,raw in sorted(zip(objs,records),key=lambda y:y[0].record_id):
        entries.append({"record_id":x.record_id,"context_id":x.context_id,"root_context_id":x.root_context_id,"domain_id":x.domain_id,"event_time":x.event_time,"known_time":x.known_time,"evidence_role":x.evidence_role,"record_hash":content_hash(raw)})
    payload={"phase":"SAED_V4_11","entries":entries,"record_count":len(entries),"future_suffix_allowed":False}
    payload['membership_id']=stable_id('membership',payload);payload['membership_hash']=content_hash(payload)
    return payload
