import copy,pytest
from saed_v4_baseline_manual.service import build_bundle
from saed_v4_baseline_manual.integrity import verify_receipt
from saed_v4_baseline_manual.errors import IntegrityError
from saed_v4_baseline_manual.replay import replay_receipt
from .helpers import program

def test_receipt_and_replay(load,upstream):
 v,h,l,t=upstream;b=build_bundle(v,h,l,t,[program(load)]);arts=[*b['compiled_programs'],*b['decision_traces'],b['baseline_registry'],b['benchmark'],b['exposure_ledger'],b['corpus_manifest'],b['telemetry']];verify_receipt(b['integrity_receipt'],arts);assert replay_receipt(b['benchmark'],b['benchmark'])['exact_match']
def test_tamper_detected(load,upstream):
 v,h,l,t=upstream;b=build_bundle(v,h,l,t,[program(load)]);arts=[*b['compiled_programs'],*b['decision_traces'],b['baseline_registry'],copy.deepcopy(b['benchmark']),b['exposure_ledger'],b['corpus_manifest'],b['telemetry']];arts[3]['baseline_count']=99
 with pytest.raises(IntegrityError):verify_receipt(b['integrity_receipt'],arts)
