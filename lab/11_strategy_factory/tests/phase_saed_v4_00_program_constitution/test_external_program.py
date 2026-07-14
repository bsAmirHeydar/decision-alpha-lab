from saed_v4_constitution.external import ExternalEvidenceClaim,evaluate_external_claim
from saed_v4_constitution.program import evaluate_program_manifest
from saed_v4_constitution.enums import DecisionStatus

def claim(cls,actual=True,hashes=('a'*64,)):
 return ExternalEvidenceClaim('c',cls,'env',hashes,actual,())

def test_static_claim_valid_when_not_executed(): assert evaluate_external_claim(claim('static',False)).status==DecisionStatus.ALLOW

def test_static_claim_cannot_assert_execution(): assert evaluate_external_claim(claim('static',True)).status==DecisionStatus.REJECT

def test_actual_claim_requires_execution(): assert evaluate_external_claim(claim('actual',False)).status==DecisionStatus.REJECT

def test_actual_claim_valid(): assert evaluate_external_claim(claim('actual',True)).status==DecisionStatus.ALLOW

def test_external_claim_needs_hash(): assert evaluate_external_claim(claim('actual',True,())).status==DecisionStatus.REJECT

def manifest():
 return {'constitution_hash':'a'*64,'objective_hash':'b'*64,'authority_matrix_hash':'c'*64,'evidence_policy_hash':'d'*64,'crosswalk_hash':'e'*64,'owners':{'primary':'p','independent_validation':'v','risk_owner':'r'},'budgets':{'hidden_submissions':1,'exposure_total':10},'status':'frozen'}

def test_program_manifest_semantic_pass(): assert evaluate_program_manifest(manifest()).status==DecisionStatus.ALLOW

def test_program_owners_must_be_independent():
 m=manifest(); m['owners']['independent_validation']='p'; assert evaluate_program_manifest(m).status==DecisionStatus.REJECT

def test_program_hashes_pinned():
 m=manifest(); m['constitution_hash']='bad'; assert evaluate_program_manifest(m).status==DecisionStatus.REJECT

def test_hidden_budget_bounded():
 m=manifest(); m['budgets']['hidden_submissions']=11; assert evaluate_program_manifest(m).status==DecisionStatus.REJECT
