---
note_id: RTHP_MT5_AUTOMATION_29_REAL_MT5_SMOKE_EVIDENCE
note_type: external_execution_evidence
status: PASS
owner: RTHP_MT5_ACTIVATION
---

# Real MT5 Smoke Train Evidence

## Evidence origin

The operator executed the one-click adapter against a connected FxPro MT5 Demo terminal using the exact broker symbols `#USSPX500` and `#USNDAQ100`.

## Verified smoke run

- Run ID: `RTHP_MT5_#USSPX500_#USNDAQ100_30F1B8FDF567`
- Source timeframe: `M1_CLOSED_BARS`
- Quality status: `PASS_WITH_DECLARED_NON_CRITICAL_GAPS`
- Train status: `PASS`
- Immutable verification status: `PASS`
- Verified file count: `33`
- Run digest: `1852f14ebfd1b26881b179b5f82ab191eb0dc0bd841293d6c5703b47a0aee2fa`
- Source binding digest: `30f1b8fdf567cc1f378cd75c7b2b087ee05f6e861e3f0803df564c35e26091be`

## Proven claims

- real terminal initialization and read-only acquisition worked;
- real broker symbols were resolved and frozen;
- closed M1 data was materialized without synthetic ticks;
- the RTHP Train Activation pipeline executed;
- generated artifacts and hashes verified;
- the central Engine and Canonical Context were not modified;
- no order or capital authority was created.

## Claims not proven by this evidence

A passing Train run does not prove predictive edge, economic value, out-of-sample stability, production readiness, or permission to trade. Those claims require the research and validation lifecycle after data activation.

## Long-horizon follow-up

The 60-day run exposed one paired Memorial Day closure. Delivery 27 classifies that interval through declared holiday and boundary evidence, allowing the long-horizon run without forward filling or threshold inflation.

## Related notes

- [[docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/RTHP_MT5_AUTOMATION/27_Holiday_and_Session_Aware_Gap_Classification]]
- [[docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/RTHP_MT5_AUTOMATION/28_Cross_Platform_Governance_Hardening]]
