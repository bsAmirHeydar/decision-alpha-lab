import copy,pytest
from saed_v4_foundation_model_adapters.authority import assert_operation
from saed_v4_foundation_model_adapters.errors import AuthorityError,BudgetError
from saed_v4_foundation_model_adapters.validation import *
from saed_v4_foundation_model_adapters.intake import decide_all
from saed_v4_foundation_model_adapters.tokenization import compile_token_sequence
from saed_v4_foundation_model_adapters.budget import enforce
@pytest.mark.parametrize('op',['predict_outcome','rank_treatment','select_treatment','allocate_risk','activate_runtime','send_order','remote_inference','online_learning'])
def test_forbidden_operations(op):
 with pytest.raises(AuthorityError):assert_operation(op)
@pytest.mark.parametrize('op',['read_frozen_graph_embeddings','materialize_reference_features','evaluate_self_supervised_objectives','register_research_checkpoint','handoff_frozen_features'])
def test_allowed_operations(op):assert assert_operation(op)
def test_budget_excess_rejected(inputs):
 cfg=validate_config(inputs['adapter_config_doc']);ins=validate_intakes(inputs['intake_docs']);cs=validate_candidates(inputs['candidate_docs'],ins);ds=validate_disclosures(inputs['disclosure_docs'],ins);dec=decide_all(ins,ds);seq=compile_token_sequence(inputs['v413_graph'],inputs['v413_embeddings'],inputs['v413_handoff']['reference_champion_id'],cfg);b=copy.deepcopy(inputs['budget_doc']);b['max_total_tokens']=1
 with pytest.raises(BudgetError):enforce(seq,cs,validate_budget(b),dec)
