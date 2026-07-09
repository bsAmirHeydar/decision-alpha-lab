# Currency Toggle Model

The runtime currency filter uses a normalized CSV string.

```text
USD,EUR,GBP,JPY,CHF,CAD,AUD,NZD,CNY
```

Clicking a currency chip removes it if present and adds it if missing.

## Why CSV Instead of Many Booleans?

The input model already uses CSV. Keeping runtime currency state as CSV means the same `GT_CsvContains()` filter path works everywhere:

- dashboard table;
- next event card;
- mini tape;
- timeline renderer;
- alert engine.
