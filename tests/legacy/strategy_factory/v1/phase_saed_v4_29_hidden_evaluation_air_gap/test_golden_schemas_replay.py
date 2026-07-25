from tools.repository_paths import find_repository_root
import copy,json
from pathlib import Path
from saed_v4_hidden_evaluation_air_gap.service import run
from saed_v4_hidden_evaluation_air_gap.canonical import content_hash
ROOT=find_repository_root(__file__); AR=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_29"
MAP={"upstream_receipt":"GOLDEN_UPSTREAM_RECEIPT.JSON","custody_receipt":"GOLDEN_CUSTODY_RECEIPT.JSON","air_gap_attestation":"GOLDEN_AIR_GAP_ATTESTATION.JSON","submission_commitment":"GOLDEN_SUBMISSION_COMMITMENT.JSON","issued_token":"GOLDEN_ISSUED_ONE_SHOT_TOKEN.JSON","consumed_token":"GOLDEN_CONSUMED_ONE_SHOT_TOKEN.JSON","sealed_result":"GOLDEN_SEALED_EVALUATION_RESULT.JSON","disclosure_envelope":"GOLDEN_DISCLOSURE_ENVELOPE.JSON","query_ledger":"GOLDEN_QUERY_LEDGER.JSON","custody_ledger":"GOLDEN_CUSTODY_LEDGER.JSON","token_ledger":"GOLDEN_TOKEN_LEDGER.JSON","transport_ledger":"GOLDEN_TRANSPORT_LEDGER.JSON","known_time_review":"KNOWN_TIME_LEAKAGE_REVIEW.JSON","security_review":"SECURITY_REVIEW.JSON","model_risk_review":"MODEL_RISK_REVIEW.JSON","authority_boundary":"GOLDEN_AUTHORITY_BOUNDARY.JSON","certificate":"GOLDEN_HIDDEN_EVALUATION_AIR_GAP_CERTIFICATE.JSON","handoff":"V4_29_TO_V4_30_HANDOFF.JSON","replay_receipt":"GOLDEN_REPLAY_RECEIPT.JSON"}
def test_all_golden_artifacts_exact(result):
    for key,name in MAP.items(): assert result[key]==json.loads((AR/name).read_text(encoding="utf-8")),name
def test_deterministic_replay(config,upstream,manifest,candidate,fixture): assert run(config,upstream,manifest,candidate,fixture)==run(config,upstream,manifest,candidate,fixture)
def test_future_suffix_invariance(config,upstream,manifest,candidate,fixture):
    a=run(config,upstream,manifest,candidate,fixture); bad=copy.deepcopy(fixture); bad["future_suffix_records"].append({"record_id":"future_999","features":{"context_signal":-999,"liquidity_state":999,"timing_alignment":-999},"hidden_label":1,"segment":"future"}); b=run(config,upstream,manifest,candidate,bad); assert a==b
def test_replay_receipt_matches(result): assert result["replay_receipt"]["output_bundle_hash"]==content_hash(result["replay_receipt"]["output_hashes"])
def test_replay_network_zero(result): assert result["replay_receipt"]["network_access"] is False
def test_replay_research_only(result): assert result["replay_receipt"]["research_only"]
