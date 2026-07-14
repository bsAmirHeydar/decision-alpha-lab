from dataclasses import replace
from fp_i15_paper import *
def test_valid_admission(proof,buy_winner,readiness): assert admit_winner(proof,buy_winner,readiness).status==AdmissionStatus.ADMITTED
def test_acceptance_required(proof,buy_winner,readiness): assert admit_winner(replace(proof,status='FAIL'),buy_winner,readiness).status==AdmissionStatus.BLOCKED
def test_config_match(proof,buy_winner,readiness): assert 'FP_PAPER_CONFIG_MISMATCH' in admit_winner(proof,replace(buy_winner,config_hash=sha256('x')),readiness).reason_codes
def test_revision_match(proof,buy_winner,readiness): assert 'FP_PAPER_SOURCE_REVISION_MISMATCH' in admit_winner(proof,replace(buy_winner,source_revision_id='REV-X'),readiness).reason_codes
def test_active_winner_required(proof,buy_winner,readiness): assert 'FP_PAPER_NOT_ACTIVE_I09_WINNER' in admit_winner(proof,buy_winner,replace(readiness,reservation_is_active_winner=False)).reason_codes
def test_watermark_required(proof,buy_winner,readiness): assert 'FP_PAPER_CAUSAL_WATERMARK_BEHIND' in admit_winner(proof,buy_winner,replace(readiness,watermark_utc_ms=0)).reason_codes
def test_complete_pair_required(proof,buy_winner,readiness): assert 'FP_PAPER_CAUSAL_DATA_INCOMPLETE' in admit_winner(proof,buy_winner,replace(readiness,secondary_complete=False)).reason_codes
