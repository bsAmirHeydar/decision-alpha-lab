from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
PY_ROOT = ROOT / "lab/11_strategy_factory/python"
EX = ROOT / "lab/11_strategy_factory/examples/saed_v4_29"
AR = ROOT / "lab/11_strategy_factory/artifacts/saed_v4_29"
if str(PY_ROOT) not in sys.path:
    sys.path.insert(0, str(PY_ROOT))

from saed_v4_hidden_evaluation_air_gap.service import run


def load(name):
    return json.loads((EX / name).read_text(encoding="utf-8"))


result = run(
    load("FULL_REFERENCE_CONFIG.JSON"),
    load("UPSTREAM_V4_28_DOCUMENTS.JSON"),
    load("PROTECTED_CUSTODY_MANIFEST.JSON"),
    load("CANDIDATE_SUBMISSION.JSON"),
    load("SEALED_SYNTHETIC_EVALUATION_FIXTURE.JSON"),
)
MAP = {
    "upstream_receipt": "GOLDEN_UPSTREAM_RECEIPT.JSON",
    "custody_receipt": "GOLDEN_CUSTODY_RECEIPT.JSON",
    "air_gap_attestation": "GOLDEN_AIR_GAP_ATTESTATION.JSON",
    "submission_commitment": "GOLDEN_SUBMISSION_COMMITMENT.JSON",
    "issued_token": "GOLDEN_ISSUED_ONE_SHOT_TOKEN.JSON",
    "consumed_token": "GOLDEN_CONSUMED_ONE_SHOT_TOKEN.JSON",
    "sealed_result": "GOLDEN_SEALED_EVALUATION_RESULT.JSON",
    "disclosure_envelope": "GOLDEN_DISCLOSURE_ENVELOPE.JSON",
    "query_ledger": "GOLDEN_QUERY_LEDGER.JSON",
    "custody_ledger": "GOLDEN_CUSTODY_LEDGER.JSON",
    "token_ledger": "GOLDEN_TOKEN_LEDGER.JSON",
    "transport_ledger": "GOLDEN_TRANSPORT_LEDGER.JSON",
    "known_time_review": "KNOWN_TIME_LEAKAGE_REVIEW.JSON",
    "security_review": "SECURITY_REVIEW.JSON",
    "model_risk_review": "MODEL_RISK_REVIEW.JSON",
    "authority_boundary": "GOLDEN_AUTHORITY_BOUNDARY.JSON",
    "certificate": "GOLDEN_HIDDEN_EVALUATION_AIR_GAP_CERTIFICATE.JSON",
    "handoff": "V4_29_TO_V4_30_HANDOFF.JSON",
    "replay_receipt": "GOLDEN_REPLAY_RECEIPT.JSON",
}
AR.mkdir(parents=True, exist_ok=True)
for key, name in MAP.items():
    (AR / name).write_text(
        json.dumps(result[key], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
print(f"V4-29 golden reproduction passed: {len(MAP)} artifacts")
