import pytest
from strategy_factory_generation import *
def make_manifest(**kw):
    d=dict(run_id='run_1',strategy_id='s1',strategy_version='1.0.0',run_mode=1,requested_generation_id=1,plugin_selection=PluginSelection('p1','1.0.0',1,''),plugin_configuration_hash='cfg_1',market_configuration_hash='mkt_1',sink_config=ResultSinkConfig(mode=SinkMode.MEMORY),git_commit='git_1',build_id='b1',environment_id='test',terminal_instance_id='t1',strict_fail_closed=True,created_at_utc_msc=1000)
    d.update(kw);return RunManifest(**d)
def test_manifest_materializes_stable_id():
    a=make_manifest().materialized();b=make_manifest().materialized();assert a.manifest_id==b.manifest_id

def test_manifest_changes_with_config():assert make_manifest(plugin_configuration_hash='cfg_2').derived_id!=make_manifest().derived_id

def test_manifest_rejects_bad_generation():
    with pytest.raises(ValueError):make_manifest(requested_generation_id=0)

def test_sink_append_only_required():
    with pytest.raises(ValueError):ResultSinkConfig(append_only=False)

def test_sink_hash_stable():assert ResultSinkConfig().config_hash==ResultSinkConfig().config_hash
