from __future__ import annotations
from pathlib import Path
from .canonical import object_digest
from .constants import CLAIM_CEILING,PHASE_ID
from .io import file_digest,load_json,load_jsonl
from .models import VerificationResult
def _check_digest(obj:dict,field:str):
    if obj.get(field)!=object_digest(obj,field): raise ValueError(f"digest mismatch: {field}")
def verify_package(repo_root:Path,package_root:Path)->VerificationResult:
    ledger=load_json(package_root/"deletion_candidate_ledger.json"); refs=load_json(package_root/"reference_proof_registry.json")
    approvals=load_json(package_root/"deletion_approval_registry.json"); blockers=load_json(package_root/"deletion_blocker_registry.json")
    handoff=load_json(package_root/"LCM15A_TO_LCM15B_HANDOFF.json"); manifest=load_json(package_root/"output_manifest.json")
    for obj,field in ((ledger,"registry_digest"),(refs,"registry_digest"),(approvals,"registry_digest"),(blockers,"registry_digest"),(handoff,"handoff_digest"),(manifest,"output_manifest_digest")): _check_digest(obj,field)
    rows=load_jsonl(package_root/ledger["records_path"]); ars=load_jsonl(package_root/approvals["records_path"]); brs=load_jsonl(package_root/blockers["records_path"])
    if len(rows)!=2168 or len(ars)!=2168: raise ValueError("candidate/approval count mismatch")
    if any(r["future_deletion_approved"] for r in rows): raise ValueError("future deletion approved")
    if any(r["deletion_performed"] for r in rows): raise ValueError("deletion performed")
    if approvals["future_deletion_approved_count"]!=0 or handoff["approved_future_deletion_count"]!=0: raise ValueError("authority boundary violated")
    if not (package_root/"approved_future_deletion_pathspec.txt").read_text(encoding="utf-8")=="": raise ValueError("future deletion pathspec must be empty")
    for r in rows:
        p=repo_root/r["candidate_path"]
        if not p.is_file() or file_digest(p)!=r["candidate_sha256"]: raise ValueError(f"candidate drift: {r['candidate_path']}")
    listed={x["path"]:x for x in manifest["files"]}
    for rel,meta in listed.items():
        p=package_root/rel
        if not p.is_file() or file_digest(p)!=meta["sha256"]: raise ValueError(f"manifest mismatch: {rel}")
    return VerificationResult(len(rows),approvals["approved_relocation_count"],blockers["deletion_blocked_candidate_count"],"PASS")
