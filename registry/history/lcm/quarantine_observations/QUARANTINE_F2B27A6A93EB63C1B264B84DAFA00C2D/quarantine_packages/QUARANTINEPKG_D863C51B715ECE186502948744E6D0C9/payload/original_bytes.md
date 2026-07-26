# Level 20 — Deployment Profile Matrix

## Purpose

This document defines practical deployment profiles for `EXEC001_STC_SMT_Cycles`.

The profile matrix is not a replacement for the EA inputs. It is an operator guide that says which groups of inputs should be enabled together and which combinations should be avoided.

## Profile summary

| Profile | Real Entry | Real Partial | Real Hard Close | Broker Scan | Alerts | Use Case |
|---|---:|---:|---:|---:|---:|---|
| Research Backtest Full Audit | No | No | No | No | No historical spam | Historical validation |
| Paper Live Observer | No | No | No | No | Yes | Live signal monitoring |
| Paper Live Broker Audit | No | No | No | Yes | Yes | Live monitoring with broker-position visibility |
| Auto Trade Entry Only Rehearsal | Yes | No | No | Yes | Yes | Controlled real-entry rehearsal |
| Auto Trade Full Managed | Yes | Yes | Yes | Yes | Yes | Full production profile |
| Emergency Hard Close Only | No | No | Yes | Yes | Yes | Close remaining magic-number positions after 15:30 |

## Common inputs across all profiles

These should be reviewed in every profile:

| Input Group | Required Decision |
|---|---|
| Symbols | `Symbol1`, `Symbol2` must be the intended pair and must be different. |
| Broker Time | Broker UTC offset must be correct. |
| Check Candle | One of 1m, 3m, 5m, 10m, 15m, 30m. |
| Strategy Switch | `Entry STC` controls new STC entries/signals for execution. |
| Partial Switch | `Partial` controls strategy partial behavior. |
| Risk | `Risk Percent`, `Final Reward`, `Contract Size`. |
| Identity | Magic number must be unique. |
| Costs | Spread/commission should be read when available; costs do not change TP geometry. |
| Validation | Validation pack should pass before auto trade. |

## Profile 1 — Research Backtest Full Audit

Intent: produce the fullest possible historical audit without touching broker positions.

Expected settings:

- Runtime mode: Research Backtest.
- Real auto-entry: off.
- Broker position manager: off or audit-only off.
- Real partial: off.
- Real hard close finalizer: off.
- Alerts: no popup/push/sound for historical backfill.
- Drawing: optional.
- All CSV audits: on.
- Validation pack: on.

Operator notes:

- Use this before every code change is trusted.
- The output is the main evidence for strategy correctness.
- Historical backfill may produce many rows, so alerts should not fire for every historical row.

## Profile 2 — Paper Live Observer

Intent: observe live STC signals and paper plans without any broker-position interaction.

Expected settings:

- Runtime mode: Paper Live.
- Real auto-entry: off.
- Broker position manager: off.
- Real partial: off.
- Real hard close finalizer: off.
- Alerts: on.
- Drawing: on.
- Persistence: on.
- Validation: on init.

Operator notes:

- This is the first live profile to use on a new broker or symbol pair.
- It should run for at least one full STC trading day before real execution is considered.

## Profile 3 — Paper Live Broker Audit

Intent: observe live STC logic and also verify that broker-position classification works.

Expected settings:

- Runtime mode: Paper Live.
- Broker position manager: on.
- Real auto-entry: off.
- Real partial: off.
- Real hard close finalizer: off.
- Allow real close in Paper Live: off.
- Alerts: on.
- Foreign-position audit: on.

Operator notes:

- Use this to confirm that manual/foreign positions are not managed.
- Useful before enabling Auto Trade.
- No real order or close should occur in this profile.

## Profile 4 — Auto Trade Entry Only Rehearsal

Intent: allow real entries, but do not yet allow real partial or hard close automation.

Expected settings:

- Runtime mode: Auto Trade.
- Broker position manager: on.
- Real auto-entry: on.
- Real partial: off.
- Real hard close finalizer: off.
- Alerts: on.
- Auto-entry grace window: small and explicit.
- Split-order cap: conservative.

Operator notes:

- This is a controlled execution rehearsal.
- Use very small risk.
- Manual supervision is required, because hard close is not automated in this profile.
- This profile is not the final production mode.

## Profile 5 — Auto Trade Full Managed

Intent: full production profile with real entry, real partial, and real hard close finalizer.

Expected settings:

- Runtime mode: Auto Trade.
- Broker position manager: on.
- Real auto-entry: on.
- Real partial: on.
- Real hard close finalizer: on.
- Partial strategy switch: on if partial is desired.
- Alerts: on.
- Validation: on init.
- Persistence: on.
- Duplicate instance lock: on.

Operator notes:

- This is the only profile intended to run the complete automated STC lifecycle.
- It should only be used after Research Backtest and Paper Live pass.
- All real actions must remain magic-only.

## Profile 6 — Emergency Hard Close Only

Intent: close remaining STC magic-number positions after 15:30 without allowing new entries.

Expected settings:

- Runtime mode: Auto Trade or Paper Live with explicit override.
- Broker position manager: on.
- Real auto-entry: off.
- Real partial: off.
- Real hard close finalizer: on.
- Entry STC: off.
- Hard close finalizer scan/retry: on.

Operator notes:

- Use only when the objective is to clean up remaining STC-managed positions.
- The finalizer must still ignore foreign/manual positions.
- If max attempts are reached, manual review is required.

## Forbidden combinations

The following combinations should be treated as invalid or extremely dangerous:

1. Real auto-entry on while broker manager is off.
2. Real partial on while broker manager is off.
3. Real hard close finalizer on while broker manager is off.
4. Paper Live with real close override enabled accidentally.
5. Duplicate EA instances with the same magic number and symbol pair.
6. Auto Trade with validation failures in time or reference matrix.
7. Auto Trade with uncertain broker UTC offset.
8. Auto Trade with Symbol1/Symbol2 set to the wrong instruments.
9. Auto Trade on a broker where tick value or contract sizing is not understood.
10. Auto Trade when manual/foreign positions on the pair are confused with STC positions.

## Minimum production checklist

Before Auto Trade Full Managed:

1. Research Backtest profile has produced clean CSV reports.
2. Paper Live Observer has run through at least M1, M2, and M3.
3. Paper Live Broker Audit has confirmed magic-only behavior.
4. Validation summary is acceptable.
5. New York time and W boundaries are visually correct.
6. Alerts match signal registry rows.
7. Broker position scan identifies only intended positions as STC-managed.
8. Emergency hard-close behavior has been reviewed on a safe account.
9. Risk percent is deliberately small for first deployment.
10. Operator understands how to immediately disable all real transports.

