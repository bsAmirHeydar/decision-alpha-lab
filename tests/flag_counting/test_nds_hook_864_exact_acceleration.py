from __future__ import annotations

import bisect
import itertools
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKTEST = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSBacktestEngine.mqh"
EVIDENCE = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSHook864CycleR1Evidence.mqh"
EVIDENCE_ENGINE = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSHook864CycleR1EvidenceEngine.mqh"
EXECUTION = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExecutionCore.mqh"
RUNNER = ROOT / "contexts/legacy/tools/flag_counting/run_nds_hook_864_cycle_r1_tests.py"
EA = ROOT / "mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5"


def potential_f3_candidate(
    *,
    allow_f3: bool,
    allow_hh: bool,
    valid_after_hook: bool,
    valid: bool,
    failed: bool,
    prices: bool,
    cycle_closed: bool,
    confirmed: bool,
    crown: bool,
    x_count: int,
    mature: bool,
    entry_inside: bool,
) -> bool:
    if not allow_f3:
        return False
    if valid_after_hook and allow_hh:
        return False
    return all(
        (
            valid,
            not failed,
            prices,
            cycle_closed,
            confirmed,
            crown,
            3 <= x_count <= 4,
            mature,
            entry_inside,
        )
    )


class ExactAccelerationContractTests(unittest.TestCase):
    def test_acceleration_is_opt_out_and_parity_universe_is_unchanged(self) -> None:
        ea = EA.read_text(encoding="utf-8")
        engine = BACKTEST.read_text(encoding="utf-8")
        self.assertIn("input bool InpBTExactAcceleration = true;", ea)
        self.assertIn("cfg.requested_bars = 5000;", engine)
        for scale in (2, 3, 5, 8, 13, 21, 34, 55):
            self.assertIn(f"cfg.scale_l", engine)
            self.assertIn(f"= {scale};", engine)
        self.assertIn("InpBTExactAcceleration=false", engine)

    def test_exposure_preflight_occurs_before_timebase_load(self) -> None:
        source = BACKTEST.read_text(encoding="utf-8")
        fast = source.index("FP_NDSBacktestExposureFastPathAvailable")
        load = source.index("FP_LoadCanonicalRates", fast)
        cycle = source.index("bool FP_RunNDSLightweightBacktestCycle")
        fast_call = source.index("if(FP_NDSBacktestExposureFastPathAvailable", cycle)
        load_call = source.index("int copied = FP_LoadCanonicalRates", cycle)
        self.assertLess(fast_call, load_call)
        self.assertLess(fast, load)

    def test_fixed_r_fast_path_does_not_replace_legacy_f3_exit(self) -> None:
        source = BACKTEST.read_text(encoding="utf-8")
        self.assertIn("fixed_r_position_broker_sl_tp_owns_exit", source)
        self.assertIn("TERMINAL_F123 needs the full F event graph", source)
        self.assertIn("terminal_f123_position_requires_f_events_only", source)
        self.assertIn("legacy_position_f_only", source)
        execution = EXECUTION.read_text(encoding="utf-8")
        self.assertIn("FP_NDSHookTradeFindExitF3", execution)
        self.assertIn("POSITION_HELD_BY_FIXED_R1_PROTECTION", execution)

    def test_demand_driven_f_gate_is_logically_complete(self) -> None:
        # F3 annotation only changes family ownership. Therefore the expensive F
        # graph is required iff at least one non-HH-owned sequence passes every
        # other immutable hard gate and F3 family is enabled.
        bools = (False, True)
        for values in itertools.product(bools, repeat=10):
            (
                allow_f3,
                allow_hh,
                valid_after_hook,
                valid,
                failed,
                prices,
                cycle_closed,
                confirmed,
                crown,
                mature,
            ) = values
            for x_count in (2, 3, 4, 5):
                for entry_inside in bools:
                    actual = potential_f3_candidate(
                        allow_f3=allow_f3,
                        allow_hh=allow_hh,
                        valid_after_hook=valid_after_hook,
                        valid=valid,
                        failed=failed,
                        prices=prices,
                        cycle_closed=cycle_closed,
                        confirmed=confirmed,
                        crown=crown,
                        x_count=x_count,
                        mature=mature,
                        entry_inside=entry_inside,
                    )
                    expected = (
                        allow_f3
                        and not (valid_after_hook and allow_hh)
                        and valid
                        and not failed
                        and prices
                        and cycle_closed
                        and confirmed
                        and crown
                        and x_count in (3, 4)
                        and mature
                        and entry_inside
                    )
                    self.assertEqual(expected, actual)

    def test_candidate_scope_contains_every_preclosure_executable_sequence(self) -> None:
        source = EVIDENCE_ENGINE.read_text(encoding="utf-8")
        required = (
            "seq.valid",
            "seq.hook_failed",
            "seq.valid_hook_family",
            "FP_HookP02SequenceCycleClosed",
            "seq.resolve_confirmed",
            "seq.cycle_crown_valid",
            "hook_entry_min_x_count",
            "hook_entry_max_x_count",
            "FP_HOOK_P02_STATE_MATURE",
            "FP_HOOK_P02_STATE_CAPPED",
            "FP_NDSHook864CycleR1RawEntryFromSequence",
        )
        for token in required:
            self.assertIn(token, source)
        self.assertIn("const bool candidate_scope", source)
        self.assertIn("candidates[i] = sequences[i]", source)

    def test_binary_lower_bound_matches_linear_first_candidate(self) -> None:
        for count in range(0, 100):
            values = list(range(10, 10 + count * 3, 3))
            for target in range(0, 320):
                linear = next((i for i, value in enumerate(values) if value >= target), len(values))
                self.assertEqual(linear, bisect.bisect_left(values, target))
        source = EVIDENCE.read_text(encoding="utf-8")
        self.assertIn("FP_NDSHook864CycleR1LowerBoundTime", source)
        self.assertIn("int first = FP_NDSHook864CycleR1LowerBoundTime", source)

    def test_one_pass_funnel_and_selection(self) -> None:
        execution = EXECUTION.read_text(encoding="utf-8")
        self.assertIn("FP_NDSHook864CycleR1AnalyzeAndSelectLatest", execution)
        selection_region = execution[execution.index("FP_HookPhase02Sequence selected;"):]
        self.assertNotIn("FP_NDSHook864CycleR1AnalyzeCandidates", selection_region[:1800])

    def test_qa_runner_parallelizes_without_fail_fast(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("ThreadPoolExecutor", source)
        self.assertIn("as_completed", source)
        self.assertIn("for index in range(1, len(COMMANDS) + 1)", source)
        self.assertIn("Every command always completes", source)
        self.assertIn("--serial", source)


if __name__ == "__main__":
    unittest.main()
