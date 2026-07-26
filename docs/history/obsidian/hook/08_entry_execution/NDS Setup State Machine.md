# NDS Setup State Machine

## Stages

```text
RESET
→ STRUCTURE_CAPTURED
→ SETUP_CANDIDATE
→ TRADE_PLAN_READY
→ COMMAND_PREVIEW_READY
```

The stage is the highest materially available object. Downstream placeholder rows do not hide the earliest upstream block.

## First-failure precedence

```text
Structure
→ Zone
→ Setup
→ Trade Plan
→ Command Preview
```

Example under the safe default:

```text
stage = STRUCTURE_CAPTURED
status = NDS_ZONE_BLOCKED_PRE_CANON_PROFILE
```

## Setup requirements

- eligible source structure;
- explicit trade-direction policy;
- available Zone;
- explicit order model;
- explicit stop model;
- explicit target model;
- trade-contract lock when required.

## Revision policy

Persistent future Setups must be append-only and revisioned. Changes in source Hook, Zone geometry, entry policy, expiry, or risk contract create a new revision rather than silently mutating audit history.

## Related

- [[NDS Structure Snapshot Contract]]
- [[NDS Trade Plan Contract]]
