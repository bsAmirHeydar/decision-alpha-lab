# Performance and Refresh

P03 performs bounded source refresh. P09 adds a source fingerprint and verification interval to avoid full object traversal every timer callback. Only the latest session snapshots influence the fingerprint, while periodic verification still detects manual object edits.

Object creation is bounded by lookback, two symbols, four sessions per trading day and maximum open charts per symbol.
