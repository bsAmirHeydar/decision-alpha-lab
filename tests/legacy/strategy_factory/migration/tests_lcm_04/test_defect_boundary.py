from tools.strategy_factory.lcm.lcm_04.io import read_json

def test_empty_register_does_not_claim_no_defects(char_root):
    d=read_json(char_root/'defects/observed_defect_register.json');assert d['record_count']==0 and not d['absence_of_record_is_absence_of_defect_claim']
def test_corrections_require_new_version(char_root): assert read_json(char_root/'defects/intended_correction_register.json')['semantic_version_bump_required']
