# Known Limitations

- Null adapters do not provide real market data.
- The terminal clock uses `TimeGMT` at seconds precision.
- No DST conversion exists yet.
- The audit bus is single-threaded and intended for the MT5 event loop.
- Service recovery after `FAILED` is not implemented.
- Candidate, model, risk and execution contracts do not yet exist.
- The Host binds null adapters; static plugin composition begins after shared market services.
- Local MetaEditor compile remains mandatory.
