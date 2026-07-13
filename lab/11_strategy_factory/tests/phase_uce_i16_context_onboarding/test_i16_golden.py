from pathlib import Path
from strategy_factory_onboarding_v3.golden import golden_run,golden_spec
from strategy_factory_onboarding_v3.enums import InvarianceStatus,ParityStatus

def test_golden_scaffold_is_repeatable():
 a=golden_run(Path('.'));b=golden_run(Path('.'))
 assert a[0].spec_hash==b[0].spec_hash
 assert a[2].manifest_hash==b[2].manifest_hash
 assert a[4].compiled_hash==b[4].compiled_hash
 assert a[3]==b[3]

def test_golden_does_not_change_core():
 r=golden_run(Path('.'));assert r[5].status is InvarianceStatus.PASS;assert not r[5].changed_core_paths

def test_golden_parity_before_migration():
 r=golden_run(Path('.'));assert r[7].status is ParityStatus.PASS;assert r[7].matched_count==5

def test_golden_wave_completes_without_destabilizing_previous():
 r=golden_run(Path('.'));assert not r[9].failed_unit_id;assert 'accepted_context' in r[9].unaffected_context_ids

def test_golden_scaffold_has_required_artifact_families():
 r=golden_run(Path('.'));assert {'schema','fixture','test','documentation','contract'}<={x.kind for x in r[2].artifacts}
