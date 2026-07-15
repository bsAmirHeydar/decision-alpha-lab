from saed_v4_sequence_state_space.service import build_reference_bundle

def test_bundle(upstream,config):
 b,s=build_reference_bundle(*upstream,*config);assert b['checkpoint_registry']['admitted_count']==6 and b['tournament']['reference_champion_id'] and b['handoff']['next_phase']=='SAED_V4_13' and len(s)==5
def test_no_authority(upstream,config):
 b,_=build_reference_bundle(*upstream,*config);c=b['claim_ledger']['claims'];assert not c['real_alpha'] and not c['treatment_selection'] and not c['production_authorization']
