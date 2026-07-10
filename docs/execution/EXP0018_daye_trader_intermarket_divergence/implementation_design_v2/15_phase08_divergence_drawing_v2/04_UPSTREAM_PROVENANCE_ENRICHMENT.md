# Upstream Provenance Enrichment

P03 now retains both the first and last occurrence of the final period High and Low:

- `high_first_time_utc`, `high_last_time_utc`
- `low_first_time_utc`, `low_last_time_utc`
- corresponding source-bar IDs

This change is evidence enrichment, not a new trading rule. P04, P05, P06, and P07 expose the P03 period store through read-only APIs. P08 also corrects accidental `c.*` aliases in the P07 Expert configuration builder so the dependency chain is compileable.
