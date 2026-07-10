from __future__ import annotations

import unittest
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Bar:
    minute: int
    high: float
    low: float


@dataclass(frozen=True)
class Proof:
    high_fresh: bool
    low_fresh: bool
    first_high_consumed_minute: int | None
    first_low_consumed_minute: int | None


def prove(reference_high: float, reference_low: float, bars: list[Bar], tick_size: float = 0.01) -> Proof:
    tolerance = max(tick_size, 1e-8) * 0.10
    high_time = next((b.minute for b in bars if b.high >= reference_high - tolerance), None)
    low_time = next((b.minute for b in bars if b.low <= reference_low + tolerance), None)
    return Proof(
        high_fresh=high_time is None,
        low_fresh=low_time is None,
        first_high_consumed_minute=high_time,
        first_low_consumed_minute=low_time,
    )


class RawPathFreshnessTests(unittest.TestCase):
    def test_adjacent_reference_has_no_intervening_consumption(self) -> None:
        self.assertEqual(prove(100.0, 90.0, []), Proof(True, True, None, None))

    def test_equal_later_high_consumes_high(self) -> None:
        proof = prove(100.0, 90.0, [Bar(1, 99.0, 95.0), Bar(2, 100.0, 94.0)])
        self.assertFalse(proof.high_fresh)
        self.assertEqual(proof.first_high_consumed_minute, 2)
        self.assertTrue(proof.low_fresh)

    def test_equal_later_low_consumes_low(self) -> None:
        proof = prove(100.0, 90.0, [Bar(1, 98.0, 92.0), Bar(2, 97.0, 90.0)])
        self.assertFalse(proof.low_fresh)
        self.assertEqual(proof.first_low_consumed_minute, 2)
        self.assertTrue(proof.high_fresh)

    def test_ndx_stale_blocks_strict_pair_even_when_spx_is_fresh(self) -> None:
        spx = prove(100.0, 90.0, [Bar(1, 99.0, 91.0)])
        ndx = prove(200.0, 180.0, [Bar(1, 201.0, 185.0)])
        self.assertTrue(spx.high_fresh)
        self.assertFalse(ndx.high_fresh)
        self.assertFalse(spx.high_fresh and ndx.high_fresh)

    def test_pair_result_is_symbol_order_invariant(self) -> None:
        spx = prove(100.0, 90.0, [Bar(1, 99.0, 91.0)])
        ndx = prove(200.0, 180.0, [Bar(1, 199.0, 181.0)])
        forward = spx.high_fresh and ndx.high_fresh
        reversed_order = ndx.high_fresh and spx.high_fresh
        self.assertEqual(forward, reversed_order)

    def test_mql_contract_contains_raw_path_and_stored_anchor_authority(self) -> None:
        root = Path(__file__).resolve().parents[3]
        confirmation = (root / "mql5/Include/IntermarketDivergenceExecution/CG/CGC_ConfirmationField.mqh").read_text(encoding="utf-8")
        drawing = (root / "mql5/Include/IntermarketDivergenceExecution/CG/CGV_Drawing.mqh").read_text(encoding="utf-8")
        self.assertIn("BuildLocalFreshnessProof", confirmation)
        self.assertIn("symbol_b_path_data_ready", confirmation)
        self.assertIn("SymbolReferenceTimeBroker", drawing)
        self.assertIn("ObjectsDeleteAll(chart_id,CGV_OBJECT_PREFIX", drawing)


if __name__ == "__main__":
    unittest.main()
