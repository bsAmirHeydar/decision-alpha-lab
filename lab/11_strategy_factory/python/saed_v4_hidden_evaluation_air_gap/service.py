from __future__ import annotations
from typing import Any
from .contracts import parse_config,parse_custody_manifest,parse_candidate,parse_fixture
from .upstream import verify as verify_upstream
from .security import scan
from .custody import verify as verify_custody,ledger as custody_ledger
from .airgap import attest,transport_ledger
from .submission import commit
from .token import issue,consume,ledger as token_ledger
from .evaluator import evaluate
from .disclosure import release
from .ledgers import query_ledger
from .audit import known_time,model_risk
from .authority import boundary
from .certificate import build as build_certificate,handoff
from .replay_receipt import build as build_replay

def run(config:dict[str,Any],upstream_documents:dict[str,Any],custody_manifest:dict[str,Any],candidate_submission:dict[str,Any],sealed_fixture:dict[str,Any])->dict[str,Any]:
    parsed=parse_config(config); manifest=parse_custody_manifest(custody_manifest,parsed["custody_policy"]); candidate=parse_candidate(candidate_submission); fixture=parse_fixture(sealed_fixture,manifest)
    security=scan(config,custody_manifest,candidate_submission)
    upstream=verify_upstream(parsed["upstream_intake"],upstream_documents)
    custody=verify_custody(manifest,fixture); air=attest(parsed["air_gap_topology"],parsed["air_gap_policy"])
    submission=commit(candidate,parsed["evaluation_protocol"],manifest["plaintext_commitment_hash"])
    issued=issue(submission,custody,"2026-07-16T09:00:00Z","2026-07-16T09:15:00Z")
    consumed=consume(issued,submission,custody,"2026-07-16T09:01:00Z")
    sealed=evaluate(candidate,fixture,parsed["evaluation_protocol"],consumed,submission)
    disclosure=release(sealed,parsed["disclosure_policy"])
    qledger=query_ledger(submission,issued,consumed,sealed,disclosure); cledger=custody_ledger(manifest,custody); tledger=token_ledger(issued,consumed); transport=transport_ledger(parsed["air_gap_topology"],submission,issued,disclosure)
    known=known_time(candidate,parsed["evaluation_protocol"],manifest,issued,sealed); risk=model_risk(sealed); authority_doc=boundary()
    evidence={"upstream_receipt":upstream,"custody_receipt":custody,"air_gap_attestation":air,"submission_commitment":submission,"issued_token":issued,"consumed_token":consumed,"sealed_result":sealed,"disclosure_envelope":disclosure,"query_ledger":qledger,"custody_ledger":cledger,"token_ledger":tledger,"transport_ledger":transport,"known_time_review":known,"security_review":security,"model_risk_review":risk}
    cert=build_certificate(evidence,authority_doc); nxt=handoff(cert)
    preliminary={**evidence,"authority_boundary":authority_doc,"certificate":cert,"handoff":nxt}
    replay=build_replay(config,manifest,candidate,fixture,preliminary)
    return {**preliminary,"replay_receipt":replay}
