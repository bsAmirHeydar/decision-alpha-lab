---
id: AIEOS2-53336F084B16
title: "Alpha Lab MQL5 Compatibility Standard"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab MQL5 Compatibility Standard

## Compiler Compatibility Baseline

MQL5 code must target the actual MetaEditor build used by the project. Generic C++ assumptions are not accepted without compilation evidence.

## String Case Mutation

`StringToUpper` and `StringToLower` mutate a writable variable and return `bool`.

Correct:

```mql5
string normalized = source;
StringToUpper(normalized);
```

Incorrect:

```mql5
string normalized = StringToUpper(source);
if(StringToLower(Clean(value)) == "true") { }
```

## Integer Serialization

Use compiler-supported conversion functions. For project compatibility, use `IntegerToString` for integer/long values unless a tested alternative is required. `LongToString` must not be assumed available.

## Timeseries

- Document whether arrays are series-indexed.
- Do not mix chronological and series indexing implicitly.
- Closed-bar logic uses shift `1` unless intrabar behavior is explicitly specified.
- `CopyRates`/`CopyBuffer` return counts must be checked before reading arrays.
- Multi-symbol data must be synchronized by time, not by assuming equal indices.

## Symbol and Chart Safety

- `SymbolSelect` and history synchronization are preconditions.
- Symbol-local prices are drawn only on the matching symbol chart.
- Object names are deterministic and owned by a module prefix.
- Cleanup deletes owned objects only.
- `ObjectCreate`, `ObjectSet*`, `ChartOpen`, and file operations are checked.

## Event and State Safety

- `OnInit` establishes contracts and fails explicitly when prerequisites are missing.
- `OnTick` must not rebuild full history without an approved budget.
- `OnTimer` work must be idempotent.
- Timeframe/symbol changes must reset or rebuild state deterministically.
- Research/anatomy experts must not call trading APIs.

## Compile Gate

Desired result is `0 errors, 0 warnings`. Warnings require written disposition. Known forbidden patterns are scanned by `tools/engineering/check_mql5_compatibility.py`.
