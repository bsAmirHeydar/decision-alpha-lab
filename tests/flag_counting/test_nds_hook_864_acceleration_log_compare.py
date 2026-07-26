from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from contexts.legacy.tools.flag_counting.compare_nds_hook_864_acceleration_logs import compare, parse_runs


class AccelerationLogCompareTests(unittest.TestCase):
    def write_log(self, text: str) -> Path:
        handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False)
        with handle:
            handle.write(text)
        return Path(handle.name)

    def test_equal_decisions_allow_different_timing_and_diagnostics(self) -> None:
        exact_path = self.write_log(
            "NDS_BT profile=PARITY status=NO_ELIGIBLE action=NONE setup_key=none "
            "entry=0.00 stop=0.00 target=0.00 reason=accelerated elapsed_us=100\n"
        )
        reference_path = self.write_log(
            "NDS_BT profile=PARITY status=NO_ELIGIBLE action=NONE setup_key=none "
            "entry=0.00 stop=0.00 target=0.00 reason=full elapsed_us=400\n"
        )
        try:
            mismatches, summary = compare(parse_runs(exact_path), parse_runs(reference_path))
            self.assertEqual([], mismatches)
            self.assertTrue(summary["decision_parity"])
            self.assertEqual(4.0, summary["speedup_x"])
            self.assertEqual(75.0, summary["wall_work_reduction_pct"])
        finally:
            exact_path.unlink(missing_ok=True)
            reference_path.unlink(missing_ok=True)

    def test_geometry_mismatch_fails_parity(self) -> None:
        exact_path = self.write_log(
            "NDS_BT status=LIMIT_SENT action=LIMIT_SENT setup_key=A entry=100 stop=90 target=110 elapsed_us=100\n"
        )
        reference_path = self.write_log(
            "NDS_BT status=LIMIT_SENT action=LIMIT_SENT setup_key=A entry=101 stop=90 target=112 elapsed_us=100\n"
        )
        try:
            mismatches, summary = compare(parse_runs(exact_path), parse_runs(reference_path))
            self.assertEqual(1, len(mismatches))
            self.assertFalse(summary["decision_parity"])
        finally:
            exact_path.unlink(missing_ok=True)
            reference_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
