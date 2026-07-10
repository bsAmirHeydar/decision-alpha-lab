# NDS Pre-Canon Contract Checklist

## Structural axis

- [ ] Post-F3 ownership compares `terminal_bar_index` to `origin_bar_index`.
- [ ] No `PeriodSeconds(_Period)` is used to infer structural bar distance.
- [ ] The copied closed-bar stream remains oldest-to-newest.

## Configuration truthfulness

- [ ] `InpHookPhase02ValidF3RequireOppositeDirection` changes classification when toggled.
- [ ] `EARLIEST_FIRST` selects the earliest canonical origin bar.
- [ ] Zero price tolerance requires exact terminal-origin price equality.
- [ ] Structural/geometric and direct/delayed switches appear in summary export.

## Ownership evidence

For every visible post-F3 Hook, verify:

- [ ] `opposing_f3_event_id` is populated.
- [ ] matched F3 terminal bar/time/price are populated.
- [ ] origin-distance bars are non-negative.
- [ ] family label agrees with direct/delayed and structural/geometric flags.

## Valid-only leakage

- [ ] invalid sequence arcs are absent.
- [ ] invalid node labels are absent.
- [ ] same-origin siblings do not leak.
- [ ] companion parent appears only for a valid Hook-after-Hook child.
- [ ] no fallback structure is drawn when no valid family exists.

## Rebuild

- [ ] timeframe change removes owned objects and reconstructs from history.
- [ ] EA reattach produces the same final Hook set.
- [ ] CSV and chart family counts reconcile.

## Known pending tests

Do not mark these as implementation defects until Canon is answered:

- exact ownership-window duration;
- required rebound path;
- 80% denominator and wick/close evidence;
- terminal confirmation bar count;
- Zone boundaries and lifecycle.
