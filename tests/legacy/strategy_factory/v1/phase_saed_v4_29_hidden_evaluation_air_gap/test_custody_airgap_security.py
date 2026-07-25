import copy,pytest
from saed_v4_hidden_evaluation_air_gap.contracts import parse_config,parse_custody_manifest,parse_fixture
from saed_v4_hidden_evaluation_air_gap.custody import verify
from saed_v4_hidden_evaluation_air_gap.airgap import attest
from saed_v4_hidden_evaluation_air_gap.security import scan
from saed_v4_hidden_evaluation_air_gap.errors import IntegrityError,SecurityError

def test_custody_commitment_verified(config,manifest,fixture):
    p=parse_config(config); m=parse_custody_manifest(manifest,p["custody_policy"]); f=parse_fixture(fixture,m); assert verify(m,f)["commitment_verified"]
def test_custody_plaintext_mutation_detected(config,manifest,fixture):
    p=parse_config(config); m=parse_custody_manifest(manifest,p["custody_policy"]); f=parse_fixture(fixture,m); f["records"][0]["hidden_label"]=1-f["records"][0]["hidden_label"]
    with pytest.raises(IntegrityError): verify(m,f)
def test_future_suffix_excluded_from_commitment(config,manifest,fixture):
    p=parse_config(config); m=parse_custody_manifest(manifest,p["custody_policy"]); f=parse_fixture(fixture,m); a=verify(m,f); f["future_suffix_records"].append(copy.deepcopy(f["future_suffix_records"][0])); b=verify(m,f); assert a["custody_receipt_hash"]==b["custody_receipt_hash"]
def test_airgap_attestation(config):
    p=parse_config(config); a=attest(p["air_gap_topology"],p["air_gap_policy"]); assert a["passed"] and a["network_egress"] is False
@pytest.mark.parametrize("key,value",[("hidden_labels",[1]),("private_key","x"),("network_url","x")])
def test_security_forbidden_keys(key,value):
    with pytest.raises(SecurityError): scan({key:value})
@pytest.mark.parametrize("text",["https://example.test","pip install package","curl secret","socket.connect","subprocess.run","os.system('x')","powershell -enc AAA"])
def test_security_forbidden_strings(text):
    with pytest.raises(SecurityError): scan({"note":text})
def test_security_clean_reference(config,candidate,manifest): assert scan(config,candidate,manifest)["passed"]
def test_result_has_zero_security_events(result):
    s=result["security_review"]; assert s["network_egress_attempts"]==0 and s["researcher_hidden_label_reads"]==0 and s["raw_result_egress_attempts"]==0
@pytest.mark.parametrize("ledger",["custody_ledger","token_ledger","query_ledger","transport_ledger"])
def test_all_ledgers_verified(result,ledger): assert result[ledger]["chain_verification"]["verified"]
def test_researcher_plaintext_access_zero(result): assert result["custody_ledger"]["researcher_plaintext_access_events"]==0
def test_transport_raw_hidden_zero(result): assert result["transport_ledger"]["raw_hidden_data_transfers"]==0
def test_transport_round_trips_zero(result): assert result["transport_ledger"]["round_trips"]==0
