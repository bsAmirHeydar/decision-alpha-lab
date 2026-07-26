# NDS Entry Audit Outputs

## Runtime files

```text
nds_entry_structure_snapshot.csv
nds_entry_setup_candidate.csv
nds_entry_trade_plan.csv
nds_entry_command_preview.csv
nds_entry_pipeline_summary.csv
```

## Traceability chain

```text
sequence_id
→ structure_key
→ zone_key
→ setup_id/setup_key
→ plan_id/plan_key
→ command_id/command_key
```

## Minimum review questions

1. Which exact Hook sequence was selected?
2. Which validity family and parent lineage did it carry?
3. Where did the pipeline first block?
4. Was the Zone canonical or diagnostic?
5. Which direction, order, stop, and target policies were active?
6. Was RR geometrically valid?
7. Did volume remain zero and `send_allowed=false`?

## Release requirement

Any future broker-adapter phase must retain this lineage and add risk authorization, broker request, transaction, fill, cancel, expiry, and reconciliation identifiers.

## Related

- [[NDS Structure Snapshot Contract]]
- [[NDS Command Preview Contract]]
