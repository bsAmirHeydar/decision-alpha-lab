from copy import deepcopy
from src.engine.tooling.strategy_factory.acl_os.acl_04.human_dsl import compile_human_setup
from src.engine.tooling.strategy_factory.acl_os.acl_04.constraints import evaluate_policy
from src.engine.tooling.strategy_factory.acl_os.acl_04.baseline import compile_baselines


def codes(findings): return {x['code'] for x in findings}

def test_valid_human_policy_has_no_blockers(fixtures):
    ir=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    assert evaluate_policy(ir,fixtures['registry'],fixtures['search'],fixtures['envelope'])==[]


def test_risk_outside_envelope_is_blocked(fixtures):
    ir=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    ir=deepcopy(ir);ir['risk_contract']['max_risk_units']=2
    assert 'ACL04_RISK_OUTSIDE_TREATMENT_ENVELOPE' in codes(evaluate_policy(ir,fixtures['registry'],fixtures['search'],fixtures['envelope']))


def test_conflicting_directions_are_blocked(fixtures):
    ir=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    ir=deepcopy(ir);cl=deepcopy(ir['clauses'][0]);cl['clause_id']='ENTRY_SHORT';cl['action']='ENTER_SHORT';ir['clauses'].append(cl)
    assert 'ACL04_CONFLICTING_ENTRY_DIRECTIONS' in codes(evaluate_policy(ir,fixtures['registry'],fixtures['search'],fixtures['envelope']))


def test_future_atom_is_not_allowed_for_human(fixtures):
    ir=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    ir=deepcopy(ir);ir['clauses'][0]['when']={'op':'ATOM','atom_id':'FUTURE_OUTCOME_IS','args':['POSITIVE']}
    result=codes(evaluate_policy(ir,fixtures['registry'],fixtures['search'],fixtures['envelope']))
    assert 'ACL04_FUTURE_DERIVED_ATOM_FORBIDDEN' in result
    assert 'ACL04_ATOM_LANE_FORBIDDEN' in result


def test_baseline_catalog_is_complete(fixtures):
    baselines=compile_baselines('CTX_REFERENCE_ALPHA','0.1.0')
    assert len(baselines)==5
    oracle=dict(baselines)['BASELINE_DIAGNOSTIC_ORACLE']
    assert oracle['diagnostic_only'] is True
    assert evaluate_policy(oracle,fixtures['registry'],fixtures['search'],fixtures['envelope'])==[]


def test_nonbaseline_expiry_is_required(fixtures):
    ir=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    ir=deepcopy(ir);ir['clauses']=[c for c in ir['clauses'] if c['kind']!='EXPIRY']
    assert 'ACL04_EXPIRY_CONTRACT_REQUIRED' in codes(evaluate_policy(ir,fixtures['registry'],fixtures['search'],fixtures['envelope']))


def test_treatment_family_must_be_inside_envelope(fixtures):
    ir=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    ir=deepcopy(ir);ir['treatment_family']='UNAUTHORIZED_TREATMENT'
    assert 'ACL04_TREATMENT_FAMILY_FORBIDDEN' in codes(evaluate_policy(ir,fixtures['registry'],fixtures['search'],fixtures['envelope']))


def test_protective_reference_contract_is_enforced(fixtures):
    ir=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    ir=deepcopy(ir);ir['risk_contract']['protective_reference_required']=False
    assert 'ACL04_PROTECTIVE_REFERENCE_REQUIRED' in codes(evaluate_policy(ir,fixtures['registry'],fixtures['search'],fixtures['envelope']))


def test_envelope_required_clause_kinds_are_enforced(fixtures):
    ir=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    ir=deepcopy(ir);ir['clauses']=[c for c in ir['clauses'] if c['kind']!='EXPIRY']
    result=codes(evaluate_policy(ir,fixtures['registry'],fixtures['search'],fixtures['envelope']))
    assert 'ACL04_REQUIRED_CLAUSE_KIND_MISSING' in result
