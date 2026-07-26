# Phase 13 Hotfix001 — MQL5 Long Serialization

## Failure

MetaEditor reported:

- undeclared identifier `LongToString`
- operator/parser failures around `size_bytes`
- implicit conversion warnings caused by the failed expression

## Diagnosis

The inventory writer serializes `SCGP13FileRow::size_bytes`, which is declared as `long`. The target MQL5 compiler does not expose `LongToString`. MQL5 `IntegerToString` accepts the long integer value and is the correct conversion function for this contract.

The additional errors were cascading parser errors. They were not independent defects in the CSV column sequence.

## Correction

```mql5
IntegerToString(rows[i].size_bytes)
```

## Invariants preserved

- CSV column order is unchanged.
- `size_bytes` remains a long in the data contract.
- File inventory semantics are unchanged.
- The Phase 12.5 readiness gate is unchanged.
- Python model-comparison execution is unchanged.
- No trading or execution authority is introduced.
