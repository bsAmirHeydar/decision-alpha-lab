# Report — H4/H5 GOLD M10 Review, 2026-06-20

This report summarizes the project findings from the GOLD M10 H4/H5 logs and the subsequent code-audit discussion.

---

## Dataset context

Instrument: GOLD  
Timeframe: M10  
Bars: approximately 21,370  
M0001 events: approximately 3,197  
Classic M0002 paired branch labels: approximately 2,484

---

## H0004 classic vs causal-batch result

The classic H4 sample sequence reported strong regime inertia:

- same-label transition rate: 72.82%,
- same lift over IID: 19.80 percentage points,
- lag-1 correlation: 0.4214.

After causal known-candle batching:

- pure known-time batches: 1,807,
- ambiguous mixed-energy batches: 40,
- same-candle batch count: 441,
- causal same-label transition rate: 65.61%,
- causal same lift: 11.98 percentage points,
- causal lag-1 correlation: 0.2584.

Interpretation:

- Same-candle sequencing was a real issue.
- The classic report overstated inertia.
- The causal effect remained meaningful after removing fake same-candle transitions.

The correct next standard is atomic no-sample replay: raw events by known time, not completed samples.

---

## H0005 classic path result

The H5 classic path report separated reversal and continuation paths.

### Reversal

Classic structural reversal path behavior:

- path count: approximately 1,544,
- realized win rate: 48.96%,
- average win: 3.59R,
- average loss: 4.86R,
- profit factor: 0.7080,
- expectancy: -0.7245R.

Fixed-reward reversal paths looked better:

- R1 win rate: 61.79%,
- R2 win rate: 48.06%.

Interpretation:

- Reversal is not a strong full structural path edge in the classic report.
- Reversal may still be a short reaction edge.
- It needs touch-entry, cost-aware, stop-aware validation.

### Continuation

Classic continuation path behavior:

- path count: approximately 657,
- realized win rate: 69.41%,
- average win: 3.49R,
- average loss: 2.05R,
- profit factor: 7.2477,
- expectancy: +2.0883R.

Code audit showed that this R was path-normalized, not a true trading R, because continuation used regime-change exit without an executed initial stop.

Interpretation:

- Continuation likely contains a real path/movement fact.
- The reported PF is not a real execution PF.
- Continuation must be retested with explicit ATR, structural, fixed-R, or trailing risk.

---

## Official conclusion

H0004 and H0005 should no longer be judged by classic sample reports alone.

Official claim level:

1. H4 memory exists in the classic report.
2. H4 memory remains after causal known-time batching, but weaker.
3. H4 must be validated with atomic no-sample raw-event replay.
4. H5 reversal is a reaction candidate, not a full-path edge by default.
5. H5 continuation is a strong path candidate, but its old PF is not tradable until explicit risk is applied.
6. Main H4/H5 Experts must default to atomic no-sample reporting.

---

## Decision impact

Execution research should split into two independent lines:

### Reversal execution

- zone touch,
- short target or first opposite zone,
- strict same-bar policy,
- spread-aware stop/entry,
- real R1/R2 reports.

### Continuation execution

- close-break or intrabar-break,
- ATR stop or structural stop,
- trailing alternatives,
- regime-change only when the change is knowable,
- separate path-R and tradable-R reports.
