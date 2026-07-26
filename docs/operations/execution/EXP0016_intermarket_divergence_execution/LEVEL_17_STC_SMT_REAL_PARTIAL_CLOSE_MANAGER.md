# LEVEL 17 — STC SMT Real Partial Close Manager

Level 17 adds a magic-only real broker partial close layer for EXEC001 STC SMT Cycles.

It is disabled by default and only closes real broker volume when the user explicitly enables real partial close and an allowed runtime mode.

Key behavior:

- scans only `Symbol1` and `Symbol2` positions with matching `InpMagicNumber`;
- applies real partial close at W4/M end for M1 and M2;
- disables M3 partial because 15:30 New York hard close has priority;
- rounds 50% close volume upward to broker step;
- fully closes tiny positions when rounded partial consumes the full volume;
- writes marker files to avoid duplicate partial after restart;
- never manages foreign/manual positions;
- does not create real entries.

Output:

- `stc_level17_real_partial_actions.csv`

Safety defaults:

- `InpEnableRealPartialClose=false`
- `InpAllowRealPartialInPaperLive=false`
- `InpRuntimeMode=STC_MODE_RESEARCH_BACKTEST`
