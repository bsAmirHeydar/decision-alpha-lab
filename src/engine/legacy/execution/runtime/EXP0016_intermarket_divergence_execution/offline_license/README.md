# Offline License Layer - EXEC001 STC SMT Cycles

This patch ports the FlagCounting Phoenix offline-license architecture to the divergence / time-cycle execution project.

## MT5 recipient inputs

The license is intentionally exposed as neutral strategy/profile fields:

```text
InpCycleModelProfile      = signed token
InpCycleOperatorMemo      = passphrase
InpCycleReferenceSeed     = hidden gate 1
InpCycleDivergenceSeed    = hidden gate 2
InpCycleExecutionSeed     = hidden gate 3
InpCycleReleaseSeed       = hidden gate 4
InpCycleCacheDepthMinutes = runtime recheck cache, minimum 1 minute
```

## Issuer command

```bash
python ops/deployment/stc_smt/offline_license_keygen.py \
  --account 12345678 \
  --server "Broker-ServerName" \
  --expires 20261231 \
  --first-name Amir \
  --middle-name Hosein \
  --last-name Heydar
```

## Saved files

By default, the issuer archive is written under:

```text
licenses/stc_smt_cycles/user0001-Amir-Hosein-Heydar/
```

The recipient only receives the `*_recipient_inputs.txt` values.
The `*_issuer_audit.json` and `*_full_record.txt` files stay private.

## Runtime behavior

`IMDEXEC001_STC_SMT_Cycles.mq5` checks the license before `g_stc_engine.Init()` and before every timer pulse.
The two EXP0015 research wrappers check the same license before batch/live-monitor execution.
If the license is absent, expired, copied to another account/server, or has wrong gates/signature, init fails or the timer pulse returns without running the engine.
