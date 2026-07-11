# Canonical Mapping Contract

| Legacy field | Canonical field |
|---|---|
| `clean_symbol` | `symbol` |
| `hunter_symbol` | `reference_symbol` |
| BUY + LOW | LONG |
| SELL + HIGH | SHORT |
| `clean_reference_price` | `reference_price` |
| `clean_stop_reference_price` | `invalidation_price` |
| `group_minutes × 60` | `timeframe_seconds` |
| cycle/reference identity | parent and cluster IDs |

The anatomy state is explicitly `exp0017_raw_divergence_candidate_unconfirmed_trade`.
