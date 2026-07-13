from dataclasses import replace

import pytest

from fp_i02_kernel.contracts import ConfirmationEvent, DivergenceCandidate
from fp_i02_kernel.enums import CandidateState, RelationCode
from fp_i02_kernel.errors import FPI02Error
from fp_i02_kernel.golden import golden_candidate, golden_confirmation, golden_hunt, golden_signal


def test_hunt_time_must_be_m1_aligned():
    hunt = golden_hunt()
    with pytest.raises(FPI02Error):
        replace(hunt, m1_open_utc_ms=hunt.m1_open_utc_ms + 1000)


def test_candidate_id_ignores_state_and_reason_but_not_semantic_axis():
    candidate = golden_candidate()
    transitioned = replace(candidate, state=CandidateState.CONFIRMED, reason_code="FP_RC_CONFIRMED_ACTIVE")
    changed_tf = replace(candidate, resolved_confirmation_timeframe_seconds=900)
    assert transitioned.candidate_id == candidate.candidate_id
    assert changed_tf.candidate_id != candidate.candidate_id


def test_cross_day_relation_requires_offset():
    candidate = golden_candidate()
    with pytest.raises(FPI02Error):
        replace(candidate, relation=RelationCode.NA, calendar_offset=0)
    valid = replace(candidate, relation=RelationCode.NA, calendar_offset=1)
    assert valid.calendar_offset == 1


def test_intraday_relation_forbids_calendar_offset():
    with pytest.raises(FPI02Error):
        replace(golden_candidate(), calendar_offset=1)


def test_confirmation_event_interval_is_closed_contract():
    confirmation = golden_confirmation()
    assert confirmation.confirmation_event_id == golden_confirmation().confirmation_event_id
    with pytest.raises(FPI02Error):
        replace(confirmation, confirmation_bar_close_utc_ms=confirmation.confirmation_bar_open_utc_ms)


def test_signal_id_ignores_suppression_reason_and_eligibility():
    signal = golden_signal()
    suppressed = replace(signal, reason_code="FP_RC_SUPPRESSED_BY_WW")
    assert suppressed.signal_id == signal.signal_id


def test_signal_id_changes_when_semantic_config_changes():
    signal = golden_signal()
    changed = replace(signal, semantic_config_hash="f" * 64)
    assert changed.signal_id != signal.signal_id
