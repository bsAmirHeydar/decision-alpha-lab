from __future__ import annotations
from pathlib import Path
from .canonical import object_digest
from .io import file_digest,load_json,load_jsonl
from .models import VerificationResult

def _digest(obj:dict,field:str):
 if obj.get(field)!=object_digest(obj,field):raise ValueError(f"digest mismatch: {field}")

def verify_package(repo_root:Path,package_root:Path)->VerificationResult:
 names={
  "root_relocation_manifest.json":"registry_digest",
  "release_registry_index.json":"registry_digest",
  "installer_locator_registry.json":"registry_digest",
  "documentation_relocation_receipts.json":"registry_digest",
  "reference_rewrite_receipt.json":"registry_digest",
  "root_allowlist.json":"registry_digest",
  "revalidated_deletion_ledger.json":"registry_digest",
  "post_relocation_reference_report.json":"report_digest",
  "root_before_after_map.json":"map_digest",
  "rollback_manifest.json":"rollback_manifest_digest",
  "LCM15B_TO_LCM15C_HANDOFF.json":"handoff_digest",
  "output_manifest.json":"output_manifest_digest",
  "reports/acceptance_report.json":"report_digest",
  "reports/hostile_review_report.json":"report_digest",
 }
 for rel,field in names.items():
  p=package_root/rel
  if not p.is_file():raise ValueError(f"missing: {rel}")
  _digest(load_json(p),field)
 root=load_json(package_root/"root_relocation_manifest.json")
 docs=load_json(package_root/"documentation_relocation_receipts.json")
 refs=load_json(package_root/"post_relocation_reference_report.json")
 reval=load_json(package_root/"revalidated_deletion_ledger.json")
 handoff=load_json(package_root/"LCM15B_TO_LCM15C_HANDOFF.json")
 root_rows=load_jsonl(package_root/root["records_path"])
 doc_rows=load_jsonl(package_root/docs["records_path"])
 reval_rows=load_jsonl(package_root/reval["records_path"])
 if len(root_rows)!=6 or len(doc_rows)!=934 or len(reval_rows)!=2168:raise ValueError("count mismatch")
 if refs["active_residual_reference_count"]!=0:raise ValueError("active references remain")
 if reval["future_deletion_approved_count"]!=0 or any(r["future_deletion_approved"] for r in reval_rows):raise ValueError("deletion approval created")
 if any(r["deletion_performed"] for r in reval_rows):raise ValueError("deletion performed")
 for r in root_rows:
  source=repo_root/r["source_path"];target=repo_root/r["canonical_target_path"]
  if not source.is_file() or not target.is_file():raise ValueError(f"root relocation missing: {r['source_path']}")
  if file_digest(source)!=r["source_sha256_before"] or file_digest(target)!=r["target_sha256_after"]:raise ValueError("root hash mismatch")
 for r in doc_rows:
  legacy=repo_root/r["legacy_path"];target=repo_root/r["canonical_target_path"]
  if not legacy.is_file() or not target.is_file():raise ValueError("documentation locator missing")
  if file_digest(legacy)!=r["redirect_stub_sha256"] or file_digest(target)!=r["canonical_target_sha256"]:raise ValueError("documentation hash mismatch")
  text=legacy.read_text(encoding="utf-8")
  if r["canonical_target_path"] not in text or "compatibility-redirect" not in text:raise ValueError("redirect malformed")
 manifest=load_json(package_root/"output_manifest.json")
 for meta in manifest["files"]:
  p=package_root/meta["path"]
  if not p.is_file() or file_digest(p)!=meta["sha256"]:raise ValueError(f"manifest mismatch: {meta['path']}")
 if handoff["deletion_performed"] or handoff["future_deletion_approved_count"]!=0:raise ValueError("handoff authority violation")
 return VerificationResult(6,934,2168,0,"PASS")
