# Level 17 — Real Partial Close Manager

## Purpose

Level 17 adds the first real broker-side partial close layer for EXEC001 STC SMT Cycles.

The layer does not create entries. Real entries remain controlled by Level 16 and remain disabled unless the user explicitly enables auto trading. Level 17 only watches already-open broker positions that belong to this STC instance and closes approximately 50% of eligible positions at the end of W4 for M1 and M2.

The owner-locked rule is:

- partial close is evaluated exactly at the end of W4 / end of the M cycle;
- delayed partial must still be recovered later if the EA was offline;
- M3 partial is disabled because 15:30 New York hard close has priority;
- partial closes about 50% of volume;
- close volume is rounded upward to broker volume step;
- tiny positions can be fully closed if rounded half-volume consumes the entire position;
- foreign/manual positions must never be managed.

## Safety Status

Default configuration is safe:

- `InpEnableRealPartialClose = false`
- `InpAllowRealPartialInPaperLive = false`
- `InpRuntimeMode = STC_MODE_RESEARCH_BACKTEST`

Therefore, applying and compiling this patch does not close any real broker position by default.

## Managed Positions

A broker position is eligible only when all conditions hold:

1. Position symbol equals `Symbol1` or `Symbol2`.
2. Position magic number equals `InpMagicNumber`.
3. Position was opened inside the current STC trading day.
4. Position was opened inside an active M cycle.
5. Position was opened in M1 or M2.
6. Partial is enabled.
7. W4/M-end partial time is due.
8. 15:30 New York hard close is not yet due.
9. The current-day partial marker for this position identifier does not already exist.
10. Real partial transport is enabled by inputs and runtime mode.

## W4 Due Times

The layer uses the same STC cycle model as the paper partial simulator:

- M1 partial due: 02:00 New York
- M2 partial due: 09:00 New York
- M3 partial: disabled because 15:30 hard close has priority

If the EA is offline at 02:00 or 09:00 and comes back before hard close, Level 17 performs delayed real partial recovery.

## Duplicate Prevention

Real partial close is destructive, so duplicate prevention is required.

When a real partial close succeeds, the layer writes a marker under Common Files:

`dal/stc/EXEC001_STC_SMT_Cycles/real_partial_markers/<stc_day_id>/partial_done_<position_identifier>.marker`

On later scans or after restart, if the marker exists, the position is skipped. If a close request fails, no marker is written, so later scans can retry.

## Volume Rule

The real close volume is computed from current broker position volume:

1. `raw_half = position_volume * 0.5`
2. `close_volume = ceil(raw_half to broker volume step)`
3. if close volume consumes the whole position, send a full position close
4. otherwise send a partial close

The layer respects broker minimum volume. If the computed partial volume cannot be safely sent, it writes an audit row and skips.

## Runtime Transport Gate

Real partial is allowed only when:

- `InpEnableBrokerPositionManager = true`
- `InpEnableRealPartialClose = true`
- broker manager requirement is satisfied
- runtime mode is `AUTO_TRADE`

Paper Live can close real volume only if explicitly enabled:

- `InpRuntimeMode = STC_MODE_PAPER_LIVE`
- `InpAllowRealPartialInPaperLive = true`

The default is false.

## Outputs

Level 17 adds:

`stc_level17_real_partial_actions.csv`

Important columns:

- ticket
- position identifier
- symbol
- position magic
- position type
- open time
- open New York time
- open M/W
- partial due time
- already marked done
- original volume
- close volume
- remaining estimate
- transport allowed
- action allowed
- action attempted
- action succeeded
- trade retcode
- status
- rule note

## Non-Goals

Level 17 does not:

- create real entries;
- change entry logic;
- manage manual positions;
- manage positions with a different magic number;
- perform M3 partial;
- replace the 15:30 hard close manager;
- alter paper journal outcomes.

## Acceptance Criteria

Level 17 is accepted when:

1. Compiles with Level 16 modules.
2. Creates `stc_level17_real_partial_actions.csv`.
3. Does not close anything by default.
4. Skips foreign/manual positions.
5. Skips M3 positions for partial.
6. Sends real partial only for matching magic positions when all safety gates are explicitly enabled.
7. Writes a marker after successful close.
8. Does not send a duplicate partial when marker exists.
9. Skips partial after hard close is due.
10. Logs every allowed, blocked, skipped, and failed action.
