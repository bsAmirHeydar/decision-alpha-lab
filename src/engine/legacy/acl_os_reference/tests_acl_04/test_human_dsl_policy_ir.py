from copy import deepcopy
import pytest
from src.engine.tooling.strategy_factory.acl_os.acl_04.human_dsl import compile_human_setup
from src.engine.tooling.strategy_factory.acl_os.acl_04.expressions import normalize_expression, walk_atoms, expression_depth
from src.engine.tooling.strategy_factory.acl_os.acl_04.errors import ContractError


def test_human_dsl_compiles(fixtures):
    ir=compile_human_setup(fixtures['human'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    assert ir['lane']=='HUMAN'
    assert ir['execution_authority']=='NONE'
    assert ir['known_time_contract']=='INHERIT_ACL03_NON_BYPASSABLE'
    assert ir['policy_ir_digest'].startswith('sha256:')
    assert [c['kind'] for c in ir['clauses']][:2]==['ENTRY','INVALIDATION']


def test_context_mismatch_rejected(fixtures):
    doc=deepcopy(fixtures['human']);doc['context_id']='CTX_OTHER'
    with pytest.raises(ContractError): compile_human_setup(doc,context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')


def test_unknown_field_rejected(fixtures):
    doc=deepcopy(fixtures['human']);doc['surprise']=1
    with pytest.raises(ContractError): compile_human_setup(doc,context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')


def test_commutative_children_are_canonical():
    a={'op':'ATOM','atom_id':'CONTEXT_STATE_IS','args':['CONFIRMED']}
    b={'op':'ATOM','atom_id':'MISSINGNESS_IS_CLEAR','args':['VIEW']}
    assert normalize_expression({'op':'ALL','children':[a,b]})==normalize_expression({'op':'ALL','children':[b,a]})


def test_expression_walk_and_depth():
    e=normalize_expression({'op':'NOT','child':{'op':'ALL','children':[{'op':'ATOM','atom_id':'A_A','args':[]},{'op':'ATOM','atom_id':'B_B','args':[]}]}})
    assert len(walk_atoms(e))==2
    assert expression_depth(e)==3

@pytest.mark.parametrize('expr',[
    {},{'op':'ALL','children':[]},{'op':'BOGUS'},{'op':'ATOM','atom_id':'A_A','args':'not-list'}
])
def test_invalid_expressions_fail(expr):
    with pytest.raises(ContractError): normalize_expression(expr)
