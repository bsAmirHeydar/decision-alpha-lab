from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_sha256,require_time_before
from .errors import ProvenanceError
from .canonical import content_hash,seal

def attest_builds(statements:list[dict],sbom:dict,cutoff:str)->dict:
    statements=require_list(statements,"build_statements",2); require_unique(statements,"statement_id","build_statements"); components={c["component_id"] for c in sbom["components"]}; out=[]
    for s in statements:
        require_exact(s,["statement_id","subject_id","subject_hash","builder_id","build_type","source_hash","materials_hash","invocation_hash","known_time","hermetic","network_disabled","synthetic_fixture"])
        if s["subject_id"] not in components: raise ProvenanceError("unknown build subject")
        for k in ["subject_hash","source_hash","materials_hash","invocation_hash"]: require_sha256(s[k],k)
        require_time_before(s["known_time"],cutoff,"build known_time")
        if not s["hermetic"] or not s["network_disabled"]: raise ProvenanceError("reference builds must be hermetic and network-disabled")
        out.append(deepcopy(s))
    return seal({"phase":"SAED_V4_35","slsa_level_claim":"reference-level-3-shape-only","statements":sorted(out,key=lambda x:x["statement_id"]),"statement_count":len(out),"external_attestation":False,"research_only":True},"v435_provenance","provenance_id","provenance_hash")

def signature_manifest(sbom:dict,signatures:list[dict],cutoff:str)->dict:
    signatures=require_list(signatures,"signatures",len(sbom["components"])); require_unique(signatures,"signature_id","signatures"); components={c["component_id"]:c for c in sbom["components"]}; seen=set(); out=[]
    for s in signatures:
        require_exact(s,["signature_id","subject_id","subject_hash","key_id","signature_digest","algorithm","known_time","revoked","synthetic_fixture"])
        if s["subject_id"] not in components or s["subject_id"] in seen: raise ProvenanceError("signature subject invalid/duplicate")
        seen.add(s["subject_id"]); require_sha256(s["subject_hash"],"subject_hash"); require_sha256(s["signature_digest"],"signature_digest"); require_time_before(s["known_time"],cutoff,"signature known_time")
        if s["revoked"] or s["algorithm"]!="SHA256-SYNTHETIC-DETACHED": raise ProvenanceError("signature invalid")
        out.append(deepcopy(s))
    complete=seen==set(components)
    if not complete: raise ProvenanceError("signature coverage incomplete")
    return seal({"phase":"SAED_V4_35","signatures":sorted(out,key=lambda x:x["subject_id"]),"signature_count":len(out),"complete_coverage":True,"cryptographic_external_verification":False,"research_only":True},"v435_signatures","manifest_id","manifest_hash")

def reproducible_build(provenance:dict,reproduction_runs:list[dict])->dict:
    reproduction_runs=require_list(reproduction_runs,"reproduction_runs",2); require_unique(reproduction_runs,"run_id","reproduction_runs")
    for r in reproduction_runs:
        require_exact(r,["run_id","lab_id","input_hash","output_hash","environment_hash","deterministic","independent_operator"])
        for k in ["input_hash","output_hash","environment_hash"]: require_sha256(r[k],k)
        if not r["deterministic"] or not r["independent_operator"]: raise ProvenanceError("reproduction run invalid")
    exact=len({r["output_hash"] for r in reproduction_runs})==1
    return seal({"phase":"SAED_V4_35","runs":sorted(deepcopy(reproduction_runs),key=lambda x:x["run_id"]),"run_count":len(reproduction_runs),"exact_output_match":exact,"provenance_hash":provenance["provenance_hash"],"external_build_reproduction":False,"research_only":True},"v435_reprobuild","receipt_id","receipt_hash")

def tamper_evidence(sbom:dict,signatures:dict,provenance:dict)->dict:
    leaves=sorted([c["content_hash"] for c in sbom["components"]]+[s["signature_digest"] for s in signatures["signatures"]]+[provenance["provenance_hash"]])
    level=leaves[:]
    while len(level)>1:
        if len(level)%2:level.append(level[-1])
        level=[content_hash({"left":level[i],"right":level[i+1]}) for i in range(0,len(level),2)]
    return seal({"phase":"SAED_V4_35","leaf_count":len(leaves),"merkle_root":level[0],"append_only":True,"tamper_detection_enabled":True,"research_only":True},"v435_tamper","receipt_id","receipt_hash")
