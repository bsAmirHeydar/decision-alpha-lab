import copy,pytest
from saed_v4_independent_multi_lab_replication.chain import verify_chain
from saed_v4_independent_multi_lab_replication.errors import IntegrityError
@pytest.mark.parametrize("ledger_key,domain",[("registration_ledger","v430_registration"),("preregistration","v430_preregistration"),("runs","v430_run"),("results","v430_result"),("adjudication","v430_adjudication")])
def test_chain_valid(result,ledger_key,domain): assert verify_chain(result[ledger_key]["records"],domain)["verified"]
@pytest.mark.parametrize("ledger_key,domain",[("registration_ledger","v430_registration"),("preregistration","v430_preregistration"),("runs","v430_run"),("results","v430_result"),("adjudication","v430_adjudication")])
@pytest.mark.parametrize("mutation",["sequence","previous_hash","chain","entry_hash"])
def test_chain_mutation_fails(result,ledger_key,domain,mutation):
 records=copy.deepcopy(result[ledger_key]["records"]); records[0][mutation]="bad" if mutation!="sequence" else 99
 with pytest.raises(IntegrityError): verify_chain(records,domain)
