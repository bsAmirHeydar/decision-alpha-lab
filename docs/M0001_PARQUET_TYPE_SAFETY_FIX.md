# M0001 Parquet Type Safety Fix

## Problem

`visual_rows` contains drawing rows where some fields are not applicable for every
row. For example, `NODE_PRICE` has `price`, while `EVENT` rows use `lower` and
`upper`. The CSV adapter can represent missing fields as blank strings, but
Parquet requires stable column types.

Typical error:

```text
ArrowInvalid: Could not convert '' with type str: tried to convert to double
Conversion failed for column price with type object
```

## Fix

Before writing Parquet, the Python bridge now normalizes DataFrames:

- numeric columns are converted with `pd.to_numeric(..., errors="coerce")`
- blank strings become nullable values
- booleans become nullable boolean columns
- non-numeric/object fields become strings

This keeps the Parquet artifacts stable while the thin CSV render adapter remains
compatible with MQL.
