from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
INDEX=ROOT/"releases/history/saed/indexes/SAED_V4_31_FILE_INDEX.txt"; LEDGER=ROOT/"releases/history/saed/hashes/SAED_V4_31_FILE_HASHES.sha256"; INVENTORY=ROOT/"releases/history/saed/inventories/SAED_V4_31_ARTIFACT_INVENTORY.csv"; MANIFEST=ROOT/"releases/history/saed/manifests/SAED_V4_31_PATCH_MANIFEST.json"
paths=[line.strip() for line in INDEX.read_text(encoding="utf-8").splitlines() if line.strip()]
assert paths==sorted(paths) and len(paths)==len(set(paths))
for path in paths: assert (ROOT/path).is_file(),f"missing indexed file: {path}"
expected={}
for line in LEDGER.read_text(encoding="utf-8").splitlines(): digest,path=line.split("  ",1); expected[path]=digest
assert set(expected)==set(paths)-{"releases/history/saed/hashes/SAED_V4_31_FILE_HASHES.sha256"}
for path,digest in expected.items(): assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,f"hash mismatch: {path}"
with INVENTORY.open(encoding="utf-8",newline="") as handle: rows=list(csv.DictReader(handle))
assert len(rows)==len(paths) and {row["path"] for row in rows}==set(paths)
manifest=json.loads(MANIFEST.read_text()); assert manifest["phase"]=="SAED_V4_31" and manifest["qa_passed"] and manifest["file_count"]==len(paths) and manifest["hash_count"]==len(expected) and manifest["next_phase"]=="SAED_V4_32"
status=json.loads((ROOT/"lab/11_strategy_factory/phase_status/SAED_V4_31.json").read_text()); qa=json.loads((ROOT/"releases/history/saed/reports/SAED_V4_31_QA_REPORT.json").read_text()); assert status["qa_passed"] and qa["passed"]
cert=json.loads((ROOT/"lab/11_strategy_factory/artifacts/saed_v4_31/GOLDEN_FORMAL_VERIFICATION_SAFETY_CASE_CERTIFICATE.JSON").read_text()); handoff=json.loads((ROOT/"lab/11_strategy_factory/artifacts/saed_v4_31/V4_31_TO_V4_32_HANDOFF.JSON").read_text())
assert cert["accepted_for_formal_verification_safety_case_research_reference"] and handoff["next_phase"]=="SAED_V4_32" and not any(handoff["authority"].values())
print(f"V4-31 delivery validation passed: {len(paths)} files, {len(expected)} hashes")
