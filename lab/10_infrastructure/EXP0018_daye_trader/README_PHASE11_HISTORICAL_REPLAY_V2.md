# EXP0018 Phase 11 — Historical Replay v2

Run the static contract and fixture checks:

```powershell
.\lab\10_infrastructure\EXP0018_daye_trader\powershell\run_exp0018_phase11_historical_replay_v2_checks.ps1 -RepoRoot "."
```

Compile `EXP0018_Daye_Historical_Replay_Anatomy.mq5`, attach it to any chart, set the broker symbols and fixed broker UTC offset, then select a New York replay range. Output files are written to MetaTrader Common Files.
