from pathlib import Path
import csv,hashlib,json
ROOT=Path(__file__).resolve().parents[3]
INDEX=ROOT/"releases/history/saed/indexes/SAED_V4_29_FILE_INDEX.txt"
LEDGER=ROOT/"releases/history/saed/hashes/SAED_V4_29_FILE_HASHES.sha256"
MANIFEST=ROOT/"releases/history/saed/manifests/SAED_V4_29_PATCH_MANIFEST.json"
QA=ROOT/"releases/history/saed/reports/SAED_V4_29_QA_REPORT.json"
INVENTORY=ROOT/"releases/history/saed/inventories/SAED_V4_29_ARTIFACT_INVENTORY.csv"
assert all(path.is_file() for path in [INDEX,LEDGER,MANIFEST,QA,INVENTORY])
paths=[line.strip() for line in INDEX.read_text(encoding="utf-8").splitlines() if line.strip()]
assert paths==sorted(paths) and len(paths)==len(set(paths))
assert not [path for path in paths if not (ROOT/path).is_file()]
assert not [path for path in paths if "__pycache__" in path or path.endswith(".pyc")]
expected={}
for line in LEDGER.read_text(encoding="utf-8").splitlines():
    if line.strip():
        digest,path=line.split("  ",1); expected[path]=digest
assert set(expected)==set(paths)-{"releases/history/saed/hashes/SAED_V4_29_FILE_HASHES.sha256"}
for path,digest in expected.items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
qa=json.loads(QA.read_text(encoding="utf-8"))
status=json.loads((ROOT/"lab/11_strategy_factory/phase_status/SAED_V4_29.json").read_text(encoding="utf-8"))
assert manifest["phase"]=="SAED_V4_29" and manifest["version"]=="1.0.0" and manifest["qa_passed"]
assert manifest["file_count"]==len(paths) and manifest["hash_count"]==len(expected)
assert qa["passed"] and status["qa_passed"] and status["python_tests"]>=140
assert status["closed_schemas"]==27 and status["obsidian_notes"]==272 and status["mql5_static_files"]==21
AR=ROOT/"lab/11_strategy_factory/artifacts/saed_v4_29"
certificate=json.loads((AR/"GOLDEN_HIDDEN_EVALUATION_AIR_GAP_CERTIFICATE.JSON").read_text(encoding="utf-8"))
handoff=json.loads((AR/"V4_29_TO_V4_30_HANDOFF.JSON").read_text(encoding="utf-8"))
issued=json.loads((AR/"GOLDEN_ISSUED_ONE_SHOT_TOKEN.JSON").read_text(encoding="utf-8"))
consumed=json.loads((AR/"GOLDEN_CONSUMED_ONE_SHOT_TOKEN.JSON").read_text(encoding="utf-8"))
sealed=json.loads((AR/"GOLDEN_SEALED_EVALUATION_RESULT.JSON").read_text(encoding="utf-8"))
release=json.loads((AR/"GOLDEN_DISCLOSURE_ENVELOPE.JSON").read_text(encoding="utf-8"))
query=json.loads((AR/"GOLDEN_QUERY_LEDGER.JSON").read_text(encoding="utf-8"))
custody=json.loads((AR/"GOLDEN_CUSTODY_LEDGER.JSON").read_text(encoding="utf-8"))
token=json.loads((AR/"GOLDEN_TOKEN_LEDGER.JSON").read_text(encoding="utf-8"))
transport=json.loads((AR/"GOLDEN_TRANSPORT_LEDGER.JSON").read_text(encoding="utf-8"))
replay=json.loads((AR/"GOLDEN_REPLAY_RECEIPT.JSON").read_text(encoding="utf-8"))
assert certificate["accepted_for_hidden_evaluation_air_gap_research_reference"] and all(certificate["gates"].values()) and certificate["research_only"]
for field in ["real_hidden_dataset_claim","external_custodian_independence_claim","os_air_gap_certification_claim","hsm_enforcement_claim","independent_replication_claim","real_alpha_claim","prospective_success_claim","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","live_trading_authority"]:
    assert certificate[field] is False,field
assert issued["maximum_uses"]==1 and issued["used_count"]==0 and consumed["used_count"]==1
assert sealed["evaluation_count"]==1 and sealed["future_suffix_records_seen"]==0 and sealed["network_access"] is False and sealed["raw_rows_exported"] is False
assert set(release)=={"evaluation_id","candidate_id","dataset_commitment_hash","protocol_id","decision","aggregate_metrics","baseline_comparison","release_hash"}
for forbidden in ["record_id","hidden_label","prediction","probability","rows","confusion_matrix","feature_vector","key_share","plaintext"]:
    assert forbidden not in str(release).lower()
for ledger in [query,custody,token,transport]: assert ledger["chain_verification"]["verified"]
assert query["evaluation_count"]==1 and query["adaptive_round_trip_count"]==0 and query["researcher_hidden_data_access_count"]==0
assert transport["round_trips"]==0 and transport["raw_hidden_data_transfers"]==0
assert replay["deterministic"] and replay["future_suffix_invariant"] and replay["network_access"] is False
assert handoff["next_phase"]=="SAED_V4_30" and handoff["research_only"] and not any(handoff["authority"].values())
assert "independent_replication_protocol" in handoff["allowed_next_work"] and "reuse_hidden_evaluation_token" in handoff["forbidden_next_work"]
with INVENTORY.open(encoding="utf-8",newline="") as handle: rows=list(csv.DictReader(handle))
assert len(rows)==len(paths) and {row["path"] for row in rows}==set(paths)
print(f"V4-29 delivery validation passed: {len(paths)} files, {len(expected)} hashes")
