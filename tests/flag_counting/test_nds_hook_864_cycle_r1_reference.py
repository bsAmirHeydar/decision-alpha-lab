from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools/flag_counting/nds_hook_864_cycle_r1_reference.py"
spec = importlib.util.spec_from_file_location("nds_hook_864_ref", MODULE_PATH)
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def positive(**changes):
    values = dict(
        valid=True,
        hook_failed=False,
        valid_hook_family=True,
        family_allowed=True,
        cycle_closed=True,
        resolve_confirmed=True,
        cycle_crown_valid=True,
        direction=m.Direction.POSITIVE,
        state=m.SequenceState.MATURE,
        x_count=3,
        origin_price=100.0,
        crown_price=200.0,
        terminal_price=130.0,
        terminal_retracement_ratio=0.90,
    )
    values.update(changes)
    return m.Sequence(**values)


def negative(**changes):
    values = dict(
        valid=True,
        hook_failed=False,
        valid_hook_family=True,
        family_allowed=True,
        cycle_closed=True,
        resolve_confirmed=True,
        cycle_crown_valid=True,
        direction=m.Direction.NEGATIVE,
        state=m.SequenceState.CAPPED,
        x_count=4,
        origin_price=200.0,
        crown_price=100.0,
        terminal_price=170.0,
        terminal_retracement_ratio=0.90,
    )
    values.update(changes)
    return m.Sequence(**values)


def positive_bars(*, touch_on_closure=False, touch_later=False):
    return (
        m.ClosedBar(1200, high=160.0, low=130.0),
        m.ClosedBar(1300, high=155.0, low=110.0 if touch_on_closure else 140.0),
        m.ClosedBar(1400, high=145.0, low=110.0 if touch_later else 120.0),
    )


def negative_bars(*, touch_on_closure=False, touch_later=False):
    return (
        m.ClosedBar(1200, high=170.0, low=140.0),
        m.ClosedBar(1300, high=190.0 if touch_on_closure else 180.0, low=145.0),
        m.ClosedBar(1400, high=190.0 if touch_later else 180.0, low=150.0),
    )


def evidence(seq=None, bars=None, **changes):
    seq = seq or positive()
    bars = bars or positive_bars()
    values = dict(
        record_valid=True,
        x_closure_candidate=True,
        x_closed=True,
        closure_time=1300,
        closure_price=140.0,
        closure_threshold_price=150.0,
        origin_return_penetrated=False,
    )
    values.update(changes)
    return m.build_phase04_evidence(seq, bars, **values)


class Hook864ReferenceTests(unittest.TestCase):
    def test_positive_projection(self):
        self.assertAlmostEqual(m.raw_entry(positive()), 113.6)

    def test_negative_projection(self):
        self.assertAlmostEqual(m.raw_entry(negative()), 186.4)

    def test_x3_intrinsic_is_eligible(self):
        self.assertEqual(
            m.intrinsic_eligibility(positive()),
            (True, "canonical_phase02_x3_or_x4_intrinsic_valid"),
        )

    def test_x4_intrinsic_is_eligible(self):
        self.assertTrue(m.intrinsic_eligibility(negative())[0])

    def test_terminal_retracement_does_not_own_first_arrival(self):
        self.assertTrue(m.intrinsic_eligibility(positive(terminal_retracement_ratio=0.99))[0])

    def test_x2_is_rejected(self):
        self.assertEqual(m.intrinsic_eligibility(positive(x_count=2, state=m.SequenceState.READY))[1], "canonical_x_count_not_3_or_4")

    def test_x5_is_rejected(self):
        self.assertEqual(m.intrinsic_eligibility(positive(x_count=5))[1], "canonical_x_count_not_3_or_4")

    def test_phase02_terminal_unavailable_is_rejected(self):
        self.assertEqual(m.intrinsic_eligibility(positive(cycle_closed=False))[1], "canonical_phase02_terminal_not_available")

    def test_unconfirmed_terminal_is_rejected(self):
        self.assertEqual(m.intrinsic_eligibility(positive(resolve_confirmed=False))[1], "canonical_terminal_not_confirmed")

    def test_missing_crown_is_rejected(self):
        self.assertEqual(m.intrinsic_eligibility(positive(cycle_crown_valid=False))[1], "canonical_cycle_crown_missing")

    def test_runtime_requires_phase04_evidence(self):
        self.assertEqual(m.runtime_eligibility(positive(), None)[1], "phase04_evidence_not_found_for_sequence")

    def test_phase04_closed_before_first_touch_is_runtime_eligible(self):
        self.assertEqual(
            m.runtime_eligibility(positive(), evidence()),
            (True, "phase04_x_closed_x3_or_x4_before_first_864_touch"),
        )

    def test_same_bar_closure_and_touch_is_rejected(self):
        ev = evidence(bars=positive_bars(touch_on_closure=True))
        self.assertTrue(ev.level_touched_after_closure)
        self.assertEqual(ev.first_touch_time, 1300)
        self.assertEqual(m.runtime_eligibility(positive(), ev)[1], "hook_864_first_arrival_already_consumed_after_closure")

    def test_later_touch_is_rejected(self):
        ev = evidence(bars=positive_bars(touch_later=True))
        self.assertEqual(ev.first_touch_time, 1400)
        self.assertEqual(m.runtime_eligibility(positive(), ev)[1], "hook_864_first_arrival_already_consumed_after_closure")

    def test_negative_same_bar_touch_is_rejected(self):
        seq = negative()
        ev = evidence(seq=seq, bars=negative_bars(touch_on_closure=True), closure_price=180.0, closure_threshold_price=150.0)
        self.assertTrue(ev.level_touched_after_closure)
        self.assertEqual(m.runtime_eligibility(seq, ev)[1], "hook_864_first_arrival_already_consumed_after_closure")

    def test_unclosed_phase04_cycle_is_rejected(self):
        ev = evidence(x_closed=False)
        self.assertEqual(m.runtime_eligibility(positive(), ev)[1], "phase04_x_cycle_not_closed")

    def test_invalid_phase04_record_is_rejected(self):
        ev = evidence(record_valid=False)
        self.assertEqual(m.runtime_eligibility(positive(), ev)[1], "phase04_record_invalid")

    def test_origin_return_death_is_rejected(self):
        ev = evidence(origin_return_penetrated=True)
        self.assertEqual(m.runtime_eligibility(positive(), ev)[1], "cycle_dead_by_origin_return_before_entry")

    def test_phase04_x_count_mismatch_is_rejected(self):
        ev = m.Phase04Evidence(True, True, True, 2, 1300, 140.0, 150.0, False, False)
        self.assertEqual(m.runtime_eligibility(positive(), ev)[1], "phase04_x_count_not_3_or_4")

    def test_first_touch_ignores_preclosure_touch(self):
        bars = (
            m.ClosedBar(1200, high=160.0, low=110.0),
            m.ClosedBar(1300, high=155.0, low=140.0),
            m.ClosedBar(1400, high=145.0, low=120.0),
        )
        self.assertEqual(
            m.first_touch_after_closure(bars, direction=m.Direction.POSITIVE, closure_time=1300, entry_price=113.6),
            (False, 0, 0.0),
        )

    def test_first_touch_sorts_bars_but_rejects_duplicate_times(self):
        bars = (m.ClosedBar(1400, 145.0, 120.0), m.ClosedBar(1300, 155.0, 140.0))
        self.assertEqual(m.first_touch_after_closure(bars, direction=m.Direction.POSITIVE, closure_time=1300, entry_price=113.6), (False, 0, 0.0))
        with self.assertRaisesRegex(ValueError, "unique_ascending_times"):
            m.first_touch_after_closure((m.ClosedBar(1300, 155, 140), m.ClosedBar(1300, 150, 130)), direction=m.Direction.POSITIVE, closure_time=1300, entry_price=113.6)

    def test_level_touch_gate_cannot_be_disabled(self):
        ok, reason = m.intrinsic_eligibility(positive(), m.Policy(require_level_untouched=False))
        self.assertFalse(ok)
        self.assertIn("untouched_86_4_gate_must_remain_enabled", reason)

    def test_phase04_gate_cannot_be_disabled(self):
        ok, reason = m.intrinsic_eligibility(positive(), m.Policy(require_phase04_x_closed=False))
        self.assertFalse(ok)
        self.assertIn("phase04_x_closed_gate_must_remain_enabled", reason)

    def test_invalid_hook_is_rejected(self):
        self.assertEqual(m.intrinsic_eligibility(positive(valid=False))[1], "canonical_hook_invalid_or_failed")

    def test_disallowed_family_is_rejected(self):
        self.assertEqual(m.intrinsic_eligibility(positive(family_allowed=False))[1], "canonical_hook_family_not_allowed")

    def test_wrong_state_is_rejected(self):
        self.assertEqual(m.intrinsic_eligibility(positive(state=m.SequenceState.READY))[1], "canonical_sequence_not_mature_or_capped")

    def test_positive_plan_is_stop_entry_target_and_at_least_one_r(self):
        plan = m.build_plan(positive(), evidence=evidence(), death_price=100.0, stop_buffer=1.0, minimum_stop_distance=0.5, tick_size=0.1)
        self.assertLess(plan.stop, plan.entry)
        self.assertLess(plan.entry, plan.target)
        self.assertGreaterEqual(plan.realized_r, 1.0)

    def test_negative_plan_is_target_entry_stop_and_at_least_one_r(self):
        seq = negative()
        ev = evidence(seq=seq, bars=negative_bars(), closure_price=180.0, closure_threshold_price=150.0)
        plan = m.build_plan(seq, evidence=ev, death_price=200.0, stop_buffer=1.0, minimum_stop_distance=0.5, tick_size=0.1)
        self.assertLess(plan.target, plan.entry)
        self.assertLess(plan.entry, plan.stop)
        self.assertGreaterEqual(plan.realized_r, 1.0)

    def test_build_plan_rejects_consumed_arrival(self):
        with self.assertRaisesRegex(ValueError, "first_arrival_already_consumed"):
            m.build_plan(positive(), evidence=evidence(bars=positive_bars(touch_on_closure=True)), death_price=100.0, stop_buffer=1.0, minimum_stop_distance=0.5, tick_size=0.1)

    def test_positive_death_must_remain_behind_cycle(self):
        with self.assertRaisesRegex(ValueError, "bullish_death_must_be_below_limit_entry"):
            m.build_plan(positive(), evidence=evidence(), death_price=150.0, stop_buffer=1.0, minimum_stop_distance=0.5, tick_size=0.1)

    def test_negative_death_must_remain_behind_cycle(self):
        seq = negative()
        ev = evidence(seq=seq, bars=negative_bars(), closure_price=180.0, closure_threshold_price=150.0)
        with self.assertRaisesRegex(ValueError, "bearish_death_must_be_above_limit_entry"):
            m.build_plan(seq, evidence=ev, death_price=150.0, stop_buffer=1.0, minimum_stop_distance=0.5, tick_size=0.1)

    def test_minimum_stop_distance_is_applied(self):
        seq = positive(origin_price=112.9, crown_price=118.0, terminal_price=114.0)
        ev = evidence(seq=seq, bars=(m.ClosedBar(1300, 117.0, 114.0),), closure_price=115.0, closure_threshold_price=115.45)
        plan = m.build_plan(seq, evidence=ev, death_price=112.9, stop_buffer=0.0, minimum_stop_distance=1.0, tick_size=0.1)
        self.assertGreaterEqual(plan.risk_distance, 1.0 - 1e-9)

    def test_policy_rejects_noncanonical_node_window(self):
        ok, reason = m.intrinsic_eligibility(positive(), m.Policy(min_x_count=2))
        self.assertFalse(ok)
        self.assertIn("approved_node_count_window", reason)

    def test_policy_rejects_noncanonical_ratio(self):
        ok, reason = m.intrinsic_eligibility(positive(), m.Policy(entry_ratio=0.86))
        self.assertFalse(ok)
        self.assertIn("approved_hook_entry_ratio_must_be_exactly_0_864", reason)

    def test_policy_rejects_noncanonical_closure_ratio(self):
        ok, reason = m.intrinsic_eligibility(positive(), m.Policy(closure_ratio=0.51))
        self.assertFalse(ok)
        self.assertIn("approved_cycle_closure_ratio_must_be_exactly_0_50", reason)

    def test_policy_rejects_unconfirmed_terminal_gate_disabled(self):
        ok, reason = m.intrinsic_eligibility(positive(), m.Policy(require_confirmed_terminal=False))
        self.assertFalse(ok)
        self.assertIn("confirmed_terminal_gate_must_remain_enabled", reason)

    def test_policy_rejects_noncanonical_r(self):
        ok, reason = m.intrinsic_eligibility(positive(), m.Policy(reward_r=2.0))
        self.assertFalse(ok)
        self.assertIn("approved_fixed_reward_must_be_exactly_1R", reason)

    def test_machine_readable_profile_contract_is_locked(self):
        path = ROOT / "lab/03_experiments/EXP_flag_counting/hook_864_cycle_r1/profile_contract.json"
        contract = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(contract["profile"], "HOOK_864_CYCLE_R1")
        self.assertEqual(contract["entry"]["ratio"], 0.864)
        self.assertEqual(contract["cycle_closure"]["owner"], "FP_HookPhase04")
        self.assertEqual(contract["cycle_closure"]["ratio"], 0.50)
        self.assertEqual(contract["node_count"]["allowed"], [3, 4])
        self.assertFalse(contract["node_count"]["origin_is_counted"])
        self.assertEqual(contract["exit"]["reward_r"], 1.0)
        self.assertFalse(contract["activation_allowed"])

    def test_golden_vectors_match_reference_geometry_and_runtime(self):
        path = ROOT / "lab/03_experiments/EXP_flag_counting/hook_864_cycle_r1/test_vectors.json"
        vectors = json.loads(path.read_text(encoding="utf-8"))["vectors"]
        by_id = {item["id"]: item for item in vectors}
        pos = by_id["POS_X3_PHASE04_CLOSED_UNTOUCHED"]
        neg = by_id["NEG_X4_PHASE04_CLOSED_UNTOUCHED"]
        pseq = positive(origin_price=pos["origin"], crown_price=pos["crown"], x_count=pos["x_count"])
        nseq = negative(origin_price=neg["origin"], crown_price=neg["crown"], x_count=neg["x_count"])
        self.assertAlmostEqual(m.raw_entry(pseq), pos["expected_entry"])
        self.assertAlmostEqual(m.raw_entry(nseq), neg["expected_entry"])
        self.assertTrue(m.runtime_eligibility(pseq, evidence(seq=pseq))[0])
        self.assertTrue(m.runtime_eligibility(nseq, evidence(seq=nseq, bars=negative_bars(), closure_price=180.0, closure_threshold_price=150.0))[0])


if __name__ == "__main__":
    unittest.main()
