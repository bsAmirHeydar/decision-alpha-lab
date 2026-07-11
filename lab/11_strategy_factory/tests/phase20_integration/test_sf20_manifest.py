from strategy_factory_integration import build_manifest, default_migration_waves, reference_config

def test_manifest_disables_live_authority():
    m=build_manifest(reference_config(),"run","gen","legacy_hash",1783795000000)
    assert m.engine_phase==20 and not m.live_authority
    assert "monitoring" in m.downstream_bindings

def test_migration_waves_are_ordered_and_unique():
    waves=default_migration_waves()
    assert [w.order for w in waves]==list(range(1,len(waves)+1))
    assert len({w.target_adapter_id for w in waves})==len(waves)
