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
        terminal_retracement_ratio=0.70,
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
        terminal_retracement_ratio=0.70,
    )
    values.update(changes)
    return m.Sequence(**values)


class Hook864ReferenceTests(unittest.TestCase):
    def test_positive_projection(self):
        self.assertAlmostEqual(m.raw_entry(positive()), 113.6)

    def test_negative_projection(self):
        self.assertAlmostEqual(m.raw_entry(negative()), 186.4)

    def test_x3_is_eligible(self):
        self.assertEqual(m.eligibility(positive()), (True, "canonical_closed_cycle_x3_or_x4_before_864"))

    def test_x4_is_eligible(self):
        self.assertTrue(m.eligibility(negative())[0])

    def test_x2_is_rejected(self):
        self.assertEqual(m.eligibility(positive(x_count=2, state=m.SequenceState.READY))[1], "canonical_x_count_not_3_or_4")

    def test_x5_is_rejected(self):
        self.assertEqual(m.eligibility(positive(x_count=5))[1], "canonical_x_count_not_3_or_4")

    def test_unclosed_cycle_is_rejected(self):
        self.assertEqual(m.eligibility(positive(cycle_closed=False))[1], "canonical_cycle_not_closed")

    def test_unconfirmed_terminal_is_rejected(self):
        self.assertEqual(m.eligibility(positive(resolve_confirmed=False))[1], "canonical_terminal_not_confirmed")

    def test_missing_crown_is_rejected(self):
        self.assertEqual(m.eligibility(positive(cycle_crown_valid=False))[1], "canonical_cycle_crown_missing")

    def test_level_reached_exactly_is_rejected(self):
        self.assertEqual(m.eligibility(positive(terminal_retracement_ratio=0.864))[1], "hook_864_level_already_reached_or_crossed")

    def test_level_crossed_is_rejected(self):
        self.assertEqual(m.eligibility(negative(terminal_retracement_ratio=0.90))[1], "hook_864_level_already_reached_or_crossed")

    def test_level_touch_gate_cannot_be_disabled(self):
        ok, reason = m.eligibility(positive(), m.Policy(require_level_untouched=False))
        self.assertFalse(ok)
        self.assertIn("untouched_86_4_gate_must_remain_enabled", reason)

    def test_invalid_hook_is_rejected(self):
        self.assertEqual(m.eligibility(positive(valid=False))[1], "canonical_hook_invalid_or_failed")

    def test_disallowed_family_is_rejected(self):
        self.assertEqual(m.eligibility(positive(family_allowed=False))[1], "canonical_hook_family_not_allowed")

    def test_wrong_state_is_rejected(self):
        self.assertEqual(m.eligibility(positive(state=m.SequenceState.READY))[1], "canonical_sequence_not_mature_or_capped")

    def test_positive_plan_is_stop_entry_target_and_at_least_one_r(self):
        plan = m.build_plan(positive(), death_price=100.0, stop_buffer=1.0, minimum_stop_distance=0.5, tick_size=0.1)
        self.assertLess(plan.stop, plan.entry)
        self.assertLess(plan.entry, plan.target)
        self.assertGreaterEqual(plan.realized_r, 1.0)

    def test_negative_plan_is_target_entry_stop_and_at_least_one_r(self):
        plan = m.build_plan(negative(), death_price=200.0, stop_buffer=1.0, minimum_stop_distance=0.5, tick_size=0.1)
        self.assertLess(plan.target, plan.entry)
        self.assertLess(plan.entry, plan.stop)
        self.assertGreaterEqual(plan.realized_r, 1.0)


    def test_positive_death_must_remain_behind_cycle(self):
        with self.assertRaisesRegex(ValueError, "bullish_death_must_be_below_limit_entry"):
            m.build_plan(positive(), death_price=150.0, stop_buffer=1.0, minimum_stop_distance=0.5, tick_size=0.1)

    def test_negative_death_must_remain_behind_cycle(self):
        with self.assertRaisesRegex(ValueError, "bearish_death_must_be_above_limit_entry"):
            m.build_plan(negative(), death_price=150.0, stop_buffer=1.0, minimum_stop_distance=0.5, tick_size=0.1)

    def test_minimum_stop_distance_is_applied(self):
        seq = positive(origin_price=112.9, crown_price=118.0, terminal_price=114.0, terminal_retracement_ratio=0.70)
        plan = m.build_plan(seq, death_price=112.9, stop_buffer=0.0, minimum_stop_distance=1.0, tick_size=0.1)
        self.assertGreaterEqual(plan.risk_distance, 1.0 - 1e-9)

    def test_policy_rejects_noncanonical_node_window(self):
        ok, reason = m.eligibility(positive(), m.Policy(min_x_count=2))
        self.assertFalse(ok)
        self.assertIn("approved_node_count_window", reason)

    def test_policy_rejects_noncanonical_ratio(self):
        ok, reason = m.eligibility(positive(), m.Policy(entry_ratio=0.86))
        self.assertFalse(ok)
        self.assertIn("approved_hook_entry_ratio_must_be_exactly_0_864", reason)

    def test_policy_rejects_unconfirmed_terminal_gate_disabled(self):
        ok, reason = m.eligibility(positive(), m.Policy(require_confirmed_terminal=False))
        self.assertFalse(ok)
        self.assertIn("confirmed_terminal_gate_must_remain_enabled", reason)

    def test_policy_rejects_noncanonical_r(self):
        ok, reason = m.eligibility(positive(), m.Policy(reward_r=2.0))
        self.assertFalse(ok)
        self.assertIn("approved_fixed_reward_must_be_exactly_1R", reason)


    def test_machine_readable_profile_contract_is_locked(self):
        path = ROOT / "lab/03_experiments/EXP_flag_counting/hook_864_cycle_r1/profile_contract.json"
        contract = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(contract["profile"], "HOOK_864_CYCLE_R1")
        self.assertEqual(contract["entry"]["ratio"], 0.864)
        self.assertEqual(contract["node_count"]["allowed"], [3, 4])
        self.assertFalse(contract["node_count"]["origin_is_counted"])
        self.assertEqual(contract["exit"]["reward_r"], 1.0)
        self.assertFalse(contract["activation_allowed"])

    def test_golden_vectors_match_reference_geometry(self):
        path = ROOT / "lab/03_experiments/EXP_flag_counting/hook_864_cycle_r1/test_vectors.json"
        vectors = json.loads(path.read_text(encoding="utf-8"))["vectors"]
        by_id = {item["id"]: item for item in vectors}
        pos = by_id["POS_X3_GOLDEN"]
        neg = by_id["NEG_X4_GOLDEN"]
        self.assertAlmostEqual(m.raw_entry(positive(
            origin_price=pos["origin"], crown_price=pos["crown"],
            x_count=pos["x_count"],
            terminal_retracement_ratio=pos["terminal_retracement_ratio"],
        )), pos["expected_entry"])
        self.assertAlmostEqual(m.raw_entry(negative(
            origin_price=neg["origin"], crown_price=neg["crown"],
            x_count=neg["x_count"],
            terminal_retracement_ratio=neg["terminal_retracement_ratio"],
        )), neg["expected_entry"])


if __name__ == "__main__":
    unittest.main()
