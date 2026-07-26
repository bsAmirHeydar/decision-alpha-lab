# FP-I09 Ledger Diagnostic Checklist

- [ ] Config/context epoch/pair hashes match.
- [ ] Consumption policy displays `UNSET` and live authority displays `NONE`.
- [ ] Event sequence is contiguous and hash chain validates.
- [ ] Duplicate signal IDs have identical semantic hash.
- [ ] One quota key exists per context epoch/trading day/pair/A-L-N session.
- [ ] Winner has minimum canonical rank key.
- [ ] All non-winners remain in the ledger with explicit disposition.
- [ ] Reservation generation and finality are visible.
- [ ] Checkpoint config, version, payload and chain head validate.
- [ ] Restart/rebuild snapshot hashes match.
