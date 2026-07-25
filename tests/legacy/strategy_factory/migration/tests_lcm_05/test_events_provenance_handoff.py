from tools.strategy_factory.lcm.lcm_05.io import read_json
from tools.strategy_factory.lcm.lcm_05.canonical import digest_object

def test_event_chain(topology_root):
    l=read_json(topology_root/'events/topology_event_ledger.json');prev=None
    for i,e in enumerate(l['events'],1):assert e['sequence']==i;assert e['previous_event_digest']==prev;assert digest_object(e,'event_digest')==e['event_digest'];prev=e['event_digest']
def test_provenance_denies_mutation(topology_root):
    p=read_json(topology_root/'provenance/topology_provenance_graph.json');assert p['reaches_lcm04_characterization'];assert not p['legacy_semantics_mutated'];assert not p['target_paths_materialized']
def test_handoff_bound(topology_root):
    h=read_json(topology_root/'handoff/lcm05_to_lcm06_handoff.json');assert h['handoff_type']=='LCM05_TO_LCM06';assert digest_object(h,'handoff_digest')==h['handoff_digest'];assert not h['target_materialization_allowed']
def test_handoff_forbids_authority(topology_root):
    h=read_json(topology_root/'handoff/lcm05_to_lcm06_handoff.json');assert 'MATERIALIZE_TARGET_PATH' in h['forbidden_actions'];assert 'AUTHORIZE_LIVE_ORDER' in h['forbidden_actions'];assert 'ACTIVATE_CAPITAL' in h['forbidden_actions']
