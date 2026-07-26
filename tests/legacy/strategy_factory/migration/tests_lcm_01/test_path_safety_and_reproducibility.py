import json
from src.engine.tooling.strategy_factory.lcm.lcm_01.config import SurveyConfig
from src.engine.tooling.strategy_factory.lcm.lcm_01.collision_scan import scan

def test_config_digest_is_stable():
    assert SurveyConfig().digest==SurveyConfig().digest

def test_casefold_collision_detection():
    records=({'path':'A/X.mqh'},{'path':'a/x.mqh'})
    r=scan(records,240); assert r['case_insensitive_collisions']

def test_unknown_is_not_pass(survey_root):
    v=json.loads((survey_root/'unknowns/unknown_registry.json').read_text())
    assert v['unknown_is_not_pass'] is True and v['unknown_is_not_authority'] is True

def test_reproducibility_excludes_mtime_and_randomness(survey_root):
    v=json.loads((survey_root/'reproducibility/scanner_manifest.json').read_text())
    assert 'FILE_MTIME' in v['excluded_nondeterministic_inputs'] and 'RANDOM_UUID' in v['excluded_nondeterministic_inputs']
