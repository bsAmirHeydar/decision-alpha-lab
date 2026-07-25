import pytest
from strategy_factory_onboarding_v3.waves import build_wave,CATALOG
from strategy_factory_onboarding_v3.migration import execute_wave
from strategy_factory_onboarding_v3.enums import MigrationWave
from strategy_factory_onboarding_v3.canonical import canonical_sha256
@pytest.mark.parametrize('wave,count',[(MigrationWave.A,2),(MigrationWave.B,6),(MigrationWave.C,4)])
def test_wave_catalog_counts(wave,count):assert len(build_wave(wave,canonical_sha256('core')).units)==count
@pytest.mark.parametrize('wave',[MigrationWave.A,MigrationWave.B,MigrationWave.C])
def test_wave_identity_repeats(wave):
 a=build_wave(wave,canonical_sha256('core'));b=build_wave(wave,canonical_sha256('core'));assert a.plan_hash==b.plan_hash
@pytest.mark.parametrize('wave',[MigrationWave.A,MigrationWave.B,MigrationWave.C])
def test_wave_can_complete(wave):
 p=build_wave(wave,canonical_sha256('core'));r=execute_wave(p,{u.unit_id:True for u in p.units},('old',));assert len(r.completed_unit_ids)==len(p.units);assert not r.stopped;assert 'old' in r.unaffected_context_ids
@pytest.mark.parametrize('wave',[MigrationWave.A,MigrationWave.B,MigrationWave.C])
def test_wave_stops_on_first_failed_parity(wave):
 p=build_wave(wave,canonical_sha256('core'));flags={u.unit_id:True for u in p.units};flags[p.units[0].unit_id]=False;r=execute_wave(p,flags,('old',));assert r.stopped and r.failed_unit_id==p.units[0].unit_id and not r.completed_unit_ids
@pytest.mark.parametrize('wave',[MigrationWave.A,MigrationWave.B,MigrationWave.C])
def test_wave_stop_after_unit_is_bounded(wave):
 base=build_wave(wave,canonical_sha256('core'));target=base.units[0].unit_id;p=build_wave(wave,canonical_sha256('core'),target);r=execute_wave(p,{u.unit_id:True for u in p.units});assert r.stopped and r.completed_unit_ids==(target,)
@pytest.mark.parametrize('wave',[MigrationWave.A,MigrationWave.B,MigrationWave.C])
def test_wave_units_have_explicit_limitations(wave):assert all('real_data_parity_required' in u.limitations for u in build_wave(wave,canonical_sha256('core')).units)
