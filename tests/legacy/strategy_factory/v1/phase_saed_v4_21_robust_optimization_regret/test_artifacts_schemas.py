from pathlib import Path
import json

def test_required_artifacts(root):
 a=root/'releases/history/strategy_factory/artifacts/saed_v4_21';required=['GOLDEN_ROBUST_OPTIMIZATION_REPORT.JSON','GOLDEN_ROBUST_CERTIFICATE.JSON','GOLDEN_REPLAY_RECEIPT.JSON','V4_21_TO_V4_22_HANDOFF.JSON','MODEL_RISK_REVIEW.JSON','SECURITY_REVIEW.JSON']
 assert all((a/x).is_file() for x in required)
def test_closed_schema_map(root):
 m=json.loads((root/'releases/history/strategy_factory/artifacts/saed_v4_21/CONTRACT_VALIDATION_MAP.JSON').read_text());assert m['closed_world'] and m['pair_count']>=35
 for p in m['pairs']:assert (root/p['document']).is_file() and (root/p['schema']).is_file()
def test_status_exists(root):assert (root/'releases/history/strategy_factory/program/status/SAED_V4_21.json').is_file()
