from __future__ import annotations
from pathlib import Path
from typing import Any
from .canonical import digest_file, digest_object, verify_embedded_digest
from .errors import ContractError, IntegrityError
from .io import load_json, safe_relative
from .policies import HANDOFF_IN, REQUIRED_UPSTREAM_ACTIONS, FORBIDDEN_UPSTREAM_INFERENCES, MAX_CANDIDATES
from .schema_validation import validate_instance

REQUIRED_PATHS={
 "handoff":"handoff/acl05_handoff.json",
 "manifest":"output_manifest.json",
 "receipt":"factory_receipt.json",
 "dedup":"reports/deduplication_report.json",
 "exposure":"reports/search_exposure_ledger.json",
 "provenance":"lineage/provenance_graph.json",
}

def _semantic(document: dict[str,Any], field: str, label: str) -> None:
    if not verify_embedded_digest(document,field): raise IntegrityError(f"invalid {label} embedded digest")

def _validate_manifest(root: Path, manifest: dict[str,Any]) -> None:
    validate_instance("acl04_output_manifest",manifest)
    _semantic(manifest,"manifest_digest","ACL04 manifest")
    files=manifest["files"]
    if len(files)!=manifest["artifact_count"]: raise IntegrityError("ACL04 artifact count mismatch")
    seen=set()
    for item in files:
        rel=item["path"]
        if rel in seen: raise IntegrityError(f"duplicate manifest path: {rel}")
        seen.add(rel); path=safe_relative(root,rel)
        if not path.is_file() or path.is_symlink(): raise IntegrityError(f"missing or unsafe ACL04 artifact: {rel}")
        if path.stat().st_size!=item["size_bytes"]: raise IntegrityError(f"size mismatch: {rel}")
        if digest_file(path)!=item["digest"]: raise IntegrityError(f"byte digest mismatch: {rel}")

def load_acl04_bundle(root: Path) -> dict[str,Any]:
    root=root.resolve()
    marker=root/".acl04_generated_root"
    if not marker.is_file() or marker.is_symlink(): raise ContractError("ACL04 generated-root marker missing")
    docs={name:load_json(safe_relative(root,rel)) for name,rel in REQUIRED_PATHS.items()}
    handoff=docs["handoff"]; manifest=docs["manifest"]; receipt=docs["receipt"]
    validate_instance("acl04_handoff_input",handoff)
    if handoff["handoff_type"]!=HANDOFF_IN: raise ContractError("wrong handoff type")
    _semantic(handoff,"handoff_digest","ACL04 handoff")
    _semantic(receipt,"receipt_digest","ACL04 receipt")
    _semantic(docs["dedup"],"report_digest","ACL04 dedup report")
    _semantic(docs["exposure"],"ledger_digest","ACL04 exposure ledger")
    _semantic(docs["provenance"],"graph_digest","ACL04 provenance graph")
    _validate_manifest(root,manifest)
    if receipt["output_manifest_digest"]!=manifest["manifest_digest"]: raise IntegrityError("receipt does not bind manifest")
    if receipt["acl05_handoff_digest"]!=handoff["handoff_digest"]: raise IntegrityError("receipt does not bind handoff")
    if handoff["deduplication_report_digest"]!=docs["dedup"]["report_digest"]: raise IntegrityError("dedup digest unbound")
    if handoff["search_exposure_ledger_digest"]!=docs["exposure"]["ledger_digest"]: raise IntegrityError("exposure digest unbound")
    if handoff["provenance_graph_digest"]!=docs["provenance"]["graph_digest"]: raise IntegrityError("provenance digest unbound")
    if set(handoff["required_acl05_actions"])!=REQUIRED_UPSTREAM_ACTIONS: raise ContractError("upstream action contract changed")
    if set(handoff["forbidden_acl05_inferences"])!=FORBIDDEN_UPSTREAM_INFERENCES: raise ContractError("upstream forbidden-inference contract changed")
    if handoff["live_order_submission_allowed"] or handoff["capital_activation_allowed"]: raise ContractError("upstream authority escalation")
    refs=handoff["candidate_references"]
    if not refs or len(refs)>MAX_CANDIDATES: raise ContractError("candidate count outside policy")
    candidates=[]; by_setup={}
    for p in sorted((root/"candidates/canonical").glob("*.json")):
        doc=load_json(p); validate_instance("acl04_candidate",doc)
        _semantic(doc,"candidate_digest",f"candidate {p.name}")
        if doc["setup_id"] in by_setup: raise IntegrityError("duplicate canonical setup id")
        by_setup[doc["setup_id"]]=doc; candidates.append(doc)
    if len(candidates)!=len(refs): raise IntegrityError("canonical candidate count mismatch")
    ref_map={r["setup_id"]:r for r in refs}
    if set(ref_map)!=set(by_setup): raise IntegrityError("handoff candidate set differs from canonical folder")
    for sid,ref in ref_map.items():
        c=by_setup[sid]
        for key in ("candidate_id","candidate_digest","behavior_digest","status"):
            if c[key]!=ref[key]: raise IntegrityError(f"candidate reference mismatch {sid}:{key}")
    if docs["exposure"].get("total_materialized")!=receipt["source_candidate_count"]: raise IntegrityError("exposure ledger incomplete")
    if docs["dedup"].get("canonical_count")!=receipt["canonical_candidate_count"]: raise IntegrityError("dedup canonical count mismatch")
    prov_text=str(docs["provenance"])
    if handoff["upstream_acl03_handoff_digest"] not in prov_text: raise IntegrityError("provenance does not reach ACL03")
    candidate_set_body=[{"setup_id":r["setup_id"],"candidate_digest":r["candidate_digest"],"behavior_digest":r["behavior_digest"],"status":r["status"]} for r in sorted(refs,key=lambda x:x["setup_id"])]
    bundle_body={"acl04_handoff_digest":handoff["handoff_digest"],"acl04_manifest_digest":manifest["manifest_digest"],"acl04_receipt_digest":receipt["receipt_digest"],"candidate_set_digest":digest_object(candidate_set_body)}
    return {**docs,"candidates":candidates,"candidate_set_digest":bundle_body["candidate_set_digest"],"bundle_digest":digest_object(bundle_body),"root":root}
