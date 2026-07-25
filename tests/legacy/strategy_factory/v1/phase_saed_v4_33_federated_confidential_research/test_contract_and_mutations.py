import copy,pytest
from saed_v4_federated_confidential_research.service import run
from saed_v4_federated_confidential_research.errors import SAEDV433Error
@pytest.mark.parametrize("mutation",["raw_export","central_access","formal_dp","real_crypto","future_manifest","bad_protocol","missing_attestation","duplicate_cell","too_high_threshold","bad_dimension","inactive_cell"])
def test_fail_closed_mutations(inputs,mutation):
 x=copy.deepcopy(inputs)
 if mutation=="raw_export":x["constitution"]["raw_data_export_allowed"]=True
 elif mutation=="central_access":x["constitution"]["central_raw_data_access_allowed"]=True
 elif mutation=="formal_dp":x["privacy_policy"]["formal_privacy_guarantee_claimed"]=True
 elif mutation=="real_crypto":x["protocols"][0]["real_cryptography_claimed"]=True
 elif mutation=="future_manifest":x["local_manifests"][0]["known_time"]="2027-01-01T00:00:00Z"
 elif mutation=="bad_protocol":x["study"]["aggregation_protocol_id"]="UNKNOWN"
 elif mutation=="missing_attestation":x["attestations"].pop()
 elif mutation=="duplicate_cell":x["cells"].append(copy.deepcopy(x["cells"][0]))
 elif mutation=="too_high_threshold":x["study"]["minimum_participants"]=10
 elif mutation=="bad_dimension":x["local_updates"][0]["vector"]=[1,2]
 elif mutation=="inactive_cell":x["cells"][0]["status"]="inactive"
 with pytest.raises(SAEDV433Error):run(x)
