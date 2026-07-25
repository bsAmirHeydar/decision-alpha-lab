from tools.repository_paths import find_repository_root
from pathlib import Path
import csv, hashlib, json

ROOT=find_repository_root(__file__)
INDEX=ROOT/"releases/history/saed/indexes/SAED_V4_27_FILE_INDEX.txt"; LEDGER=ROOT/"releases/history/saed/hashes/SAED_V4_27_FILE_HASHES.sha256"; MANIFEST=ROOT/"releases/history/saed/manifests/SAED_V4_27_PATCH_MANIFEST.json"; QA=ROOT/"releases/history/saed/reports/SAED_V4_27_QA_REPORT.json"; INVENTORY=ROOT/"releases/history/saed/inventories/SAED_V4_27_ARTIFACT_INVENTORY.csv"
assert all(p.is_file() for p in [INDEX,LEDGER,MANIFEST,QA,INVENTORY])
paths=[line.strip() for line in INDEX.read_text(encoding="utf-8").splitlines() if line.strip()]
assert paths==sorted(paths) and len(paths)==len(set(paths))
assert not [p for p in paths if not (ROOT/p).is_file()]
assert not [p for p in paths if "__pycache__" in p or p.endswith(".pyc")]
expected={}
for line in LEDGER.read_text(encoding="utf-8").splitlines():
    if line.strip():
        digest,path=line.split("  ",1); expected[path]=digest
assert set(expected)==set(paths)-{"releases/history/saed/hashes/SAED_V4_27_FILE_HASHES.sha256"}
for path,digest in expected.items(): assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
manifest=json.loads(MANIFEST.read_text(encoding="utf-8")); qa=json.loads(QA.read_text(encoding="utf-8")); status=json.loads((ROOT/"releases/history/strategy_factory/program/status/SAED_V4_27.json").read_text(encoding="utf-8"))
assert manifest["phase"]=="SAED_V4_27" and manifest["version"]=="1.0.0" and manifest["qa_passed"]
assert manifest["file_count"]==len(paths) and manifest["hash_count"]==len(expected)
assert qa["passed"] and status["qa_passed"] and status["python_tests"]==136 and status["closed_schemas"]==25 and status["obsidian_notes"]==247 and status["mql5_static_files"]==16
A=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_27"
cert=json.loads((A/"GOLDEN_COMPLETE_SEARCH_EXPOSURE_CERTIFICATE.JSON").read_text(encoding="utf-8")); handoff=json.loads((A/"V4_27_TO_V4_28_HANDOFF.JSON").read_text(encoding="utf-8")); trial=json.loads((A/"GOLDEN_COMPLETE_TRIAL_LEDGER.JSON").read_text(encoding="utf-8")); exposure=json.loads((A/"GOLDEN_COMPLETE_EXPOSURE_LEDGER.JSON").read_text(encoding="utf-8")); universe=json.loads((A/"GOLDEN_MULTIPLICITY_UNIVERSE.JSON").read_text(encoding="utf-8")); audit=json.loads((A/"GOLDEN_COMPLETENESS_AUDIT.JSON").read_text(encoding="utf-8")); integrity=json.loads((A/"GOLDEN_INTEGRITY_REPORT.JSON").read_text(encoding="utf-8")); replay=json.loads((A/"GOLDEN_REPLAY_RECEIPT.JSON").read_text(encoding="utf-8"))
assert cert["accepted_for_complete_ledger_research"] and all(cert["gates"].values()) and cert["research_only"]
for field in ("real_alpha_claim","prospective_success_claim","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","online_fdr_claim","hidden_evaluation_air_gap_claim"): assert cert[field] is False,field
assert trial["complete"] and trial["observed_trial_count"]==36 and trial["event_count"]==144 and not trial["missing_trial_ids"] and not trial["orphan_trial_ids"] and not trial["nonterminal_trial_ids"]
assert exposure["complete"] and exposure["event_count"]==44
for field in ("hidden_evaluation_queries","protected_evidence_exposures","runtime_compilations","order_submissions","online_policy_mutations","network_requests"): assert exposure[field]==0,field
assert universe["complete_materially_related_universe"] and universe["family_count"]==6 and universe["selection_risk_ready"]
assert audit["passed"] and integrity["passed"] and replay["deterministic"] and replay["network_access"] is False
assert handoff["next_phase"]=="SAED_V4_28" and handoff["research_only"] and not any(handoff["authority"].values())
assert set(handoff["allowed_next_work"])=={"alpha_investing_rule","online_fdr_wealth_ledger","anytime_valid_p_values","hypothesis_family_allocation","alpha_spending_policy","wealth_replenishment_policy","rejection_ledger","stopping_rule_registry"}
with INVENTORY.open(encoding="utf-8",newline="") as handle: rows=list(csv.DictReader(handle))
assert len(rows)==len(paths) and {r["path"] for r in rows}==set(paths)
print(f"V4-27 delivery validation passed: {len(paths)} files, {len(expected)} hashes")
