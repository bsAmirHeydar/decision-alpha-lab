# Python API Reference

## Import

```python
from strategy_factory_contracts import (
    AnatomyEvent, FeatureSnapshot, FeatureValue, MarketTimestamp,
    Direction, FeatureType, FeatureQuality,
)
```

## Immutability

The Python mirror uses frozen, slotted dataclasses. Changes produce a new object. `with_derived_id()` returns a copy containing the deterministic ID.

## Validation

Construction validates identifiers, geometry, causality, tagged value types, duplicate features, and IDs. Invalid records raise `ContractValidationError`.

## Research ingestion

A production importer should parse the wire payload, construct the mirror object, verify the supplied ID, attach artifact lineage, and only then append the row to a canonical dataset. Raw invalid rows go to quarantine.

## Stable identity

Do not call Python `hash()`. It is process-dependent. Use `stable_id()` and the exact canonical payload supplied by the contract type.

## Package priority

This package is not allowed to become the live truth. If Python behavior differs from MQL5 golden output, the discrepancy is a contract defect to resolve—not an opportunity for Python to silently correct terminal events.
