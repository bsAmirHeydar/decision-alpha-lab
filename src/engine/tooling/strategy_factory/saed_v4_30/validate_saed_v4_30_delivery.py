from __future__ import annotations
from tools.repository_paths import find_repository_root
import csv,hashlib,json
from pathlib import Path
ROOT=find_repository_root(__file__)
INDEX=ROOT/"releases/history/saed/indexes/SAED_V4_30_FILE_INDEX.txt"
LEDGER=ROOT/"releases/history/saed/hashes/SAED_V4_30_FILE_HASHES.sha256"
INVENTORY=ROOT/"releases/history/saed/inventories/SAED_V4_30_ARTIFACT_INVENTORY.csv"
MANIFEST=ROOT/"releases/history/saed/manifests/SAED_V4_30_PATCH_MANIFEST.json"
paths=[line.strip() for line in INDEX.read_text(encoding="utf-8").splitlines() if line.strip()]
assert paths==sorted(paths) and len(paths)==len(set(paths))
for path in paths:
 candidate=ROOT/path
 assert candidate.is_file(),f"missing indexed file: {path}"
expected={}
for line in LEDGER.read_text(encoding="utf-8").splitlines():
 digest,path=line.split("  ",1); expected[path]=digest
assert set(expected)==set(paths)-{"releases/history/saed/hashes/SAED_V4_30_FILE_HASHES.sha256"}
for path,digest in expected.items():
 observed=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
 assert observed==digest,f"hash mismatch: {path}"
with INVENTORY.open(encoding="utf-8",newline="") as handle: rows=list(csv.DictReader(handle))
assert len(rows)==len(paths) and {row["path"] for row in rows}==set(paths)
manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
assert manifest["phase"]=="SAED_V4_30" and manifest["version"]=="1.0.0" and manifest["qa_passed"]
assert manifest["file_count"]==len(paths) and manifest["hash_count"]==len(expected)
assert manifest["next_phase"]=="SAED_V4_31"
status=json.loads((ROOT/"releases/history/strategy_factory/program/status/SAED_V4_30.json").read_text(encoding="utf-8"))
qa=json.loads((ROOT/"releases/history/saed/reports/SAED_V4_30_QA_REPORT.json").read_text(encoding="utf-8"))
assert status["qa_passed"] and qa["passed"] and status["python_tests"]>=200
assert status["closed_schema_pairs"]==25 and status["obsidian_notes"]==272 and status["mql5_static_files"]==22
ar=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_30"
certificate=json.loads((ar/"GOLDEN_INDEPENDENT_MULTI_LAB_REPLICATION_CERTIFICATE.JSON").read_text(encoding="utf-8"))
handoff=json.loads((ar/"V4_30_TO_V4_31_HANDOFF.JSON").read_text(encoding="utf-8"))
assert certificate["accepted_for_independent_multi_lab_replication_research_reference"] and certificate["research_only"]
assert certificate["synthetic_laboratory_fixture_claim"]
for field in ["real_external_lab_independence_claim","external_institutional_replication_claim","external_signature_claim","physical_separation_claim","real_alpha_claim","prospective_success_claim","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","live_trading_authority"]: assert certificate[field] is False,field
assert handoff["next_phase"]=="SAED_V4_31" and handoff["research_only"] and not any(handoff["authority"].values())
assert "formal_invariant_catalog" in handoff["allowed_next_work"]
assert "claim_external_replication_from_synthetic_fixture" in handoff["forbidden_next_work"]
for name in ["GOLDEN_REGISTRATION_LEDGER.JSON","GOLDEN_PREREGISTRATION_LEDGER.JSON","GOLDEN_RUN_LEDGER.JSON","GOLDEN_RESULT_LEDGER.JSON","GOLDEN_ADJUDICATION_LEDGER.JSON"]:
 ledger=json.loads((ar/name).read_text(encoding="utf-8")); assert ledger["chain_verification"]["verified"]
semantic=json.loads((ar/"GOLDEN_SEMANTIC_HASH_RECONCILIATION.JSON").read_text(encoding="utf-8"))
metrics=json.loads((ar/"GOLDEN_METRIC_TOLERANCE_RECONCILIATION.JSON").read_text(encoding="utf-8"))
disagreement=json.loads((ar/"GOLDEN_REPLICATION_DISAGREEMENT_REPORT.JSON").read_text(encoding="utf-8"))
assert semantic["all_match"] and semantic["unique_semantic_hashes"]==1
assert metrics["all_within_tolerance"] and metrics["baseline_preserved"]
assert disagreement["accepted"] and disagreement["unresolved_disagreements"]==0
print(f"V4-30 delivery validation passed: {len(paths)} files, {len(expected)} hashes")
