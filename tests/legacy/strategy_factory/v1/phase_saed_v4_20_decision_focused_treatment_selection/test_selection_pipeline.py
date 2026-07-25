import copy,pytest
from saed_v4_decision_focused_treatment_selection.service import select_treatments
from saed_v4_decision_focused_treatment_selection.validation import validate_result
from saed_v4_decision_focused_treatment_selection.pareto import pareto_frontier
from saed_v4_decision_focused_treatment_selection.objectives import objective_score,decision_loss
from saed_v4_decision_focused_treatment_selection.contracts import RiskContract,SelectionPolicyContract

def test_golden_pipeline_valid(golden_result):assert validate_result(golden_result)
def test_golden_best_candidate(golden_result):assert golden_result['ranking'][0]['treatment_id']=='T_BALANCED'
def test_golden_abstains_to_skip(golden_result):assert golden_result['decision']['abstain'] and golden_result['decision']['selected_treatments']==['SKIP']
def test_pareto_is_nonempty(golden_result):assert golden_result['pareto_treatments']
def test_baselines_preserved(golden_result):assert golden_result['baseline_report']['baseline_preserved'];assert golden_result['baseline_report']['canonical_baseline']=='MANUAL_CORE'
def test_certificate_is_non_executable(golden_result):
 c=golden_result['certificate'];assert c['research_only'] and not c['runtime_executable'] and not c['decision_authority'] and not c['promotion_authority'] and not c['execution_authority']
@pytest.mark.parametrize('objective',[ 'expected_utility','lower_confidence_utility','cvar_utility','minimax_regret','pareto_robust','hybrid'])
def test_each_objective_is_finite(golden_result,config,objective):
 r=RiskContract.from_mapping(config['risk']);row=golden_result['ranking'][0];assert isinstance(objective_score(row,objective,r),float)
def test_decision_loss():assert decision_loss('A',{'A':1.0,'B':1.5})==0.5
def test_pareto_reference():
 rows=[{'treatment_id':'A','robust_utility':1,'lower_confidence_utility':1,'negative_maximum_regret':-1,'negative_complexity':-1},{'treatment_id':'B','robust_utility':0,'lower_confidence_utility':0,'negative_maximum_regret':-2,'negative_complexity':-2}];assert pareto_frontier(rows)==('A',)
def test_support_failure_disallows_candidate(config,context,outcomes,proofs,upstream_hashes):
 c=copy.deepcopy(context);c['support']['T_BALANCED']=0;r=select_treatments(config,c,outcomes,proofs,upstream_hashes);row=next(x for x in r['candidate_rows'] if x['treatment_id']=='T_BALANCED');assert not row['allowed']
def test_proof_failure_disallows_candidate(config,context,outcomes,proofs,upstream_hashes):
 c=copy.deepcopy(context);c['proof_hashes']['T_BALANCED']='tampered';r=select_treatments(config,c,outcomes,proofs,upstream_hashes);row=next(x for x in r['candidate_rows'] if x['treatment_id']=='T_BALANCED');assert not row['allowed']
def test_deterministic_repeated_selection(config,context,outcomes,proofs,upstream_hashes):
 a=select_treatments(config,context,outcomes,proofs,upstream_hashes);b=select_treatments(config,context,outcomes,proofs,upstream_hashes);assert a==b
