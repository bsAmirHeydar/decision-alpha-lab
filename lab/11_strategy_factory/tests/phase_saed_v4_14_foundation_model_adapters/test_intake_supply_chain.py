import copy
from saed_v4_foundation_model_adapters.validation import validate_intakes,validate_disclosures
from saed_v4_foundation_model_adapters.intake import decide_all
from saed_v4_foundation_model_adapters.supply_chain import attest

def test_reference_intakes_admitted(inputs):
 i=validate_intakes(inputs['intake_docs']);d=validate_disclosures(inputs['disclosure_docs'],i);rows=decide_all(i,d);assert all(x['decision']=='admit_reference' for x in rows)
def test_opaque_external_intake_quarantined(inputs):
 docs=copy.deepcopy(inputs['intake_docs']);docs[1].update(source_kind='external_checkpoint',synthetic_reference_adapter=False,exact_corpus_disclosed=False,overlap_risk='unknown');disc=copy.deepcopy(inputs['disclosure_docs']);disc[1].update(exact_corpus_disclosed=False,market_data_possible=True,evaluation_period_overlap_possible=True)
 i=validate_intakes(docs);d=validate_disclosures(disc,i);assert decide_all(i,d)[1]['decision']=='quarantine'
def test_attestation_no_external_load(inputs):
 i=validate_intakes(inputs['intake_docs'])[0];d={'decision':'admit_reference'};a=attest(i,d);assert not a['external_weights_loaded'] and not a['external_network_calls']
