from tools.repository_paths import find_repository_root
from pathlib import Path
import csv,hashlib,json
ROOT=find_repository_root(__file__)
INDEX=ROOT/"releases/history/saed/indexes/SAED_V4_28_FILE_INDEX.txt"; LEDGER=ROOT/"releases/history/saed/hashes/SAED_V4_28_FILE_HASHES.sha256"; MANIFEST=ROOT/"releases/history/saed/manifests/SAED_V4_28_PATCH_MANIFEST.json"; QA=ROOT/"releases/history/saed/reports/SAED_V4_28_QA_REPORT.json"; INVENTORY=ROOT/"releases/history/saed/inventories/SAED_V4_28_ARTIFACT_INVENTORY.csv"
assert all(p.is_file() for p in [INDEX,LEDGER,MANIFEST,QA,INVENTORY])
paths=[x.strip() for x in INDEX.read_text(encoding="utf-8").splitlines() if x.strip()]
assert paths==sorted(paths) and len(paths)==len(set(paths))
assert not [p for p in paths if not (ROOT/p).is_file()]
assert not [p for p in paths if "__pycache__" in p or p.endswith(".pyc")]
expected={}
for line in LEDGER.read_text(encoding="utf-8").splitlines():
    if line.strip():
        digest,path=line.split("  ",1); expected[path]=digest
assert set(expected)==set(paths)-{"releases/history/saed/hashes/SAED_V4_28_FILE_HASHES.sha256"}
for path,digest in expected.items(): assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
manifest=json.loads(MANIFEST.read_text(encoding="utf-8")); qa=json.loads(QA.read_text(encoding="utf-8")); status=json.loads((ROOT/"releases/history/strategy_factory/program/status/SAED_V4_28.json").read_text(encoding="utf-8"))
assert manifest["phase"]=="SAED_V4_28" and manifest["version"]=="1.0.0" and manifest["qa_passed"]
assert manifest["file_count"]==len(paths) and manifest["hash_count"]==len(expected)
assert qa["passed"] and status["qa_passed"] and status["python_tests"]==124 and status["closed_schemas"]==22 and status["obsidian_notes"]==261 and status["mql5_static_files"]==20
A=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_28"
cert=json.loads((A/"GOLDEN_ANYTIME_VALID_ONLINE_FDR_CERTIFICATE.JSON").read_text(encoding="utf-8")); handoff=json.loads((A/"V4_28_TO_V4_29_HANDOFF.JSON").read_text(encoding="utf-8")); evidence=json.loads((A/"GOLDEN_ANYTIME_EVIDENCE_REGISTRY.JSON").read_text(encoding="utf-8")); wealth=json.loads((A/"GOLDEN_ONLINE_FDR_WEALTH_LEDGER.JSON").read_text(encoding="utf-8")); rejection=json.loads((A/"GOLDEN_REJECTION_LEDGER.JSON").read_text(encoding="utf-8")); audit=json.loads((A/"GOLDEN_ONLINE_FDR_AUDIT.JSON").read_text(encoding="utf-8")); replay=json.loads((A/"GOLDEN_REPLAY_RECEIPT.JSON").read_text(encoding="utf-8"))
assert cert["accepted_for_online_fdr_research_reference"] and all(cert["gates"].values()) and cert["research_only"]
for field in ["real_world_fdr_guarantee_claim","real_alpha_claim","prospective_success_claim","hidden_evaluation_air_gap_claim","independent_replication_claim","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority"]: assert cert[field] is False,field
assert evidence["record_count"]==36 and evidence["future_look_count_discarded"]==3 and evidence["future_suffix_invariant"]
assert wealth["entry_count"]==36 and wealth["all_wealth_nonnegative"] and wealth["chain_verification"]["verified"]
assert rejection["rejection_count"]==12 and rejection["all_thresholds_crossed"] and rejection["chain_verification"]["verified"]
assert audit["passed"] and audit["synthetic_empirical_fdp"]==0.0 and audit["real_world_fdr_guarantee"] is False
assert replay["deterministic"] and replay["network_access"] is False and replay["future_suffix_invariant"]
assert handoff["next_phase"]=="SAED_V4_29" and handoff["research_only"] and not any(handoff["authority"].values())
with INVENTORY.open(encoding="utf-8",newline="") as h: rows=list(csv.DictReader(h))
assert len(rows)==len(paths) and {r["path"] for r in rows}==set(paths)
print(f"V4-28 delivery validation passed: {len(paths)} files, {len(expected)} hashes")
