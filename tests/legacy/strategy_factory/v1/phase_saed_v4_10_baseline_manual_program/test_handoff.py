from saed_v4_baseline_manual.service import build_bundle
from .helpers import program

def test_v411_handoff_is_self_supervised_only(load,upstream):
 v,h,l,t=upstream;x=build_bundle(v,h,l,t,[program(load)])['handoff'];assert x['next_phase']=='SAED_V4_11';assert x['entry_gates']['outcomes_excluded_from_pretraining_inputs'];assert not x['entry_gates']['training_authority_granted'];assert not x['authority']['use_outcomes_as_pretraining_inputs'];assert not x['authority']['select_treatment']
