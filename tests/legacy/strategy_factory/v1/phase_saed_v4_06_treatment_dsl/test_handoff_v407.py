from .helpers import build
from saed_v4_treatment_dsl.handoff import build_v4_07_handoff
from saed_v4_treatment_dsl.integrity import build_integrity_receipt
def test_handoff_is_bounded():
 p=build();h=build_v4_07_handoff(p,build_integrity_receipt(p));assert h['next_phase']=='SAED_V4_07';assert h['authority']['solve_bounded_action_lattice'];assert not h['authority']['select_treatment'];assert not h['authority']['send_order']
def test_handoff_program_hashes_exact():
 p=build();h=build_v4_07_handoff(p,build_integrity_receipt(p));assert h['program_hashes']==sorted(x.program_hash for x in p.programs)
