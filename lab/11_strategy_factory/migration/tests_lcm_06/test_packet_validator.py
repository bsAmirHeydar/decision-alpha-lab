import copy,json
from tools.strategy_factory.lcm.lcm_06.packet_validator import validate_packet
def packets(repo_root):
    return [json.loads(x) for x in (repo_root/"lab/11_strategy_factory/migration/fixtures/lcm_06/packets/reference_migration_packets.jsonl").read_text().splitlines() if x]
def test_valid_packet(repo_root): assert validate_packet(packets(repo_root)[0])["validation_status"]=="VALID_REFERENCE"
def test_ambiguous_blocks(repo_root): assert validate_packet(packets(repo_root)[1])["validation_status"]=="BLOCKED_AMBIGUITY"
def test_missing_owner_blocks(repo_root): assert "OWNER_MISSING" in validate_packet(packets(repo_root)[2])["reason_codes"]
def test_future_aware_blocks(repo_root): assert "FUTURE_AWARE_EVIDENCE_BLOCKED" in validate_packet(packets(repo_root)[3])["reason_codes"]
def test_security_review_blocks(repo_root): assert validate_packet(packets(repo_root)[4])["validation_status"]=="BLOCKED_SECURITY_REVIEW"
def test_authority_escalation_invalid(repo_root):
    p=copy.deepcopy(packets(repo_root)[0]);p["live_order_authorized"]=True;r=validate_packet(p);assert "AUTHORITY_ESCALATION" in r["reason_codes"] and not r["valid"]
def test_invalid_transition(repo_root):
    p=copy.deepcopy(packets(repo_root)[0]);p["proposed_state"]="CUTOVER";assert "INVALID_STATE_TRANSITION" in validate_packet(p)["reason_codes"]
def test_unsafe_path(repo_root):
    p=copy.deepcopy(packets(repo_root)[0]);p["target_path"]="../escape";assert "UNSAFE_PATH" in validate_packet(p)["reason_codes"]

def test_packet_digest_tamper_invalid(repo_root):
    p=copy.deepcopy(packets(repo_root)[0]);p["owner_role"]="ALTERED";r=validate_packet(p);assert "PACKET_DIGEST_INVALID" in r["reason_codes"] and not r["valid"]

def test_source_hash_mismatch_invalid(repo_root):
    p=copy.deepcopy(packets(repo_root)[0]);lookup={p["source_artifact_path"]:"sha256:"+"0"*64};r=validate_packet(p,lookup);assert "SOURCE_HASH_MISMATCH" in r["reason_codes"]

def test_source_not_in_topology_invalid(repo_root):
    p=copy.deepcopy(packets(repo_root)[0]);r=validate_packet(p,{});assert "SOURCE_NOT_IN_TOPOLOGY" in r["reason_codes"]

def test_missing_evidence_reference_invalid(repo_root):
    p=copy.deepcopy(packets(repo_root)[0]);p["evidence_refs"]=[];r=validate_packet(p);assert "EVIDENCE_REFERENCES_INCOMPLETE" in r["reason_codes"]

def test_unknown_known_time_blocks(repo_root):
    p=copy.deepcopy(packets(repo_root)[0]);p["known_time_status"]="UNKNOWN";r=validate_packet(p);assert r["validation_status"]=="BLOCKED_UNKNOWN"
