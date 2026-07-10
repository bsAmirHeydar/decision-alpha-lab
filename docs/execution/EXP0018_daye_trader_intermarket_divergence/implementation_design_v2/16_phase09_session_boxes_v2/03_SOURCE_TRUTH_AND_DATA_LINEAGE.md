# Source Truth and Data Lineage

Each box traces to one `DAYE_SymbolPeriodSnapshot`. The lineage chain is:

`broker bars → P02 symbol-local bars → P03 session snapshot → P09 projection → OBJ_RECTANGLE`.

The snapshot ID, period instance, trading-day key, broker symbol, canonical symbol, completeness and availability time remain attached to the projection and optional CSV ledger. A chart object without this lineage is not considered valid P09 evidence.
