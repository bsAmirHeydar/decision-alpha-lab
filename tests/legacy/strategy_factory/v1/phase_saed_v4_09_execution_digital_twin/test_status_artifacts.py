from conftest import load

def test_status_blocks_production_claims():
    s=load('releases/history/strategy_factory/program/status/SAED_V4_09.json');assert s['implementation_status']=='implemented_reference';assert not s['claims']['real_alpha'];assert not s['claims']['production_authorization'];assert s['external_evidence']['metaeditor_compile']=='pending_local_windows'
