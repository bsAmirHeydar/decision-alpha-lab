from saed_v4_graph_hypergraph_models.service import build_reference_bundle
def build(inputs):return build_reference_bundle(inputs['graph'],inputs['receipt'],inputs['handoff'],inputs['registry'],inputs['distill'],inputs['snapshots'],inputs['spec'],inputs['candidates'],inputs['objectives'],inputs['envelope'])
def test_bundle_replay(inputs):
 a=build(inputs);b=build(inputs);assert a['bundle_hash']==b['bundle_hash'] and a['replay_receipt']['passed']
def test_registry(inputs):
 b=build(inputs);assert b['checkpoint_registry']['admitted_count']==6 and b['checkpoint_registry']['immutable']
def test_handoff(inputs):
 b=build(inputs);assert b['handoff']['next_phase']=='SAED_V4_14' and all(b['handoff']['entry_gates'].values())
def test_no_authority(inputs):
 b=build(inputs);assert not b['claim_ledger']['claims']['production_authorization'] and not b['authority_boundary']['execution_authority']
