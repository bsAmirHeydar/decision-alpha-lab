from .helpers import build,load
def test_golden_package_hash_matches_fixture():
 assert build().package_hash == load('golden_treatment_dsl_package.json')['package_hash']
def test_golden_has_three_programs_and_one_binding():
 p=build(); assert len(p.programs)==3; assert len(p.bindings)==1
def test_golden_descriptor_binding_is_exact():
 b=build().bindings[0]; assert b.descriptor_id=='treatment_approved_001'; assert b.status.value=='bound'
def test_no_authority_claims_in_limitations():
 text=' '.join(build().limitations).lower(); assert 'does not solve' in text; assert 'order authority' in text
