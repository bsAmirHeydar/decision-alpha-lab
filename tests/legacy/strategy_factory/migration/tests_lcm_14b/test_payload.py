import json
from src.engine.tooling.strategy_factory.lcm.lcm_14b.canonical import file_digest
def test_payload_hashes(qroot):
 rows=[json.loads(x) for x in (qroot/"records/quarantine_package_records.jsonl").read_text().splitlines()]
 assert all(file_digest(qroot/r["quarantine_payload_path"])==r["original_bytes_sha256"] for r in rows)
