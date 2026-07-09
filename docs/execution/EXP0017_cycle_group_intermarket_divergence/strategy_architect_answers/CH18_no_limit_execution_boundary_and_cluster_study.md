# CH18 — No-Limit Execution Boundary and Position Cluster Study

## Boundary Statement

The base strategy has no execution limit except divergence invalidation. This chapter formalizes what this means and what must be studied later.

---

## No-Limit Fields

The strategy has no base limit on:

| Field | Base Rule |
|---|---|
| Total open positions | No limit |
| Positions per CG | No limit |
| Positions per cycle | No limit |
| Positions per clean symbol | No limit |
| Positions per hunter symbol | No limit |
| Positions per direction | No limit |
| Buy and sell at same time | Allowed |
| Same-CG repeated entries | Allowed |
| Entries after a loss | Allowed |
| Entries after a win | Allowed |
| Hedging | Allowed |
| Conflict between CGs | Allowed for raw study |

---

## Base Execution Permission

A signal can be executed if:

1. a valid reference exists;
2. one symbol hunted the reference;
3. the other symbol did not hunt its corresponding reference;
4. the active candle closed;
5. the divergence is still valid at that close;
6. the clean symbol remains clean;
7. no double-hunt invalidation occurred.

No additional restriction is applied.

---

## Position Cluster Types

### Same-CG Cluster

Multiple positions from the same CG are open simultaneously.

### Multi-CG Cluster

Positions from different CGs are open simultaneously.

### Same-Direction Cluster

Multiple positions share the same direction.

### Opposite-Direction Cluster

Buy and sell positions coexist.

### Same-Symbol Cluster

Multiple positions are open on the same clean symbol.

### Cross-Symbol Cluster

Positions are open on both symbols.

### Post-Loss Cluster

A new position opens after one or more recent losses.

### Post-Win Cluster

A new position opens after one or more recent wins.

---

## Base Doctrine Versus Future Constraint

The base doctrine says:

> allow all confirmed non-invalidated signals.

The future constraint layer may later say:

> certain clusters should be limited.

But this must be proven.

---

## Statistical Risk Fields

To understand no-limit execution, future reports should include:

- open trade count at entry;
- same-CG open trade count;
- opposite-direction open trade count;
- hedge flag;
- total open R risk;
- daily cumulative risk;
- maximum simultaneous risk;
- maximum cluster drawdown;
- cluster final outcome;
- cluster stop streak;
- cluster recovery behavior;
- signal sequence number in day;
- signal sequence number inside CG;
- prior signal outcome;
- prior same-CG outcome;
- prior same-symbol outcome.

---

## Future Constraint Promotion

A constraint can be considered only if it improves at least one of these without destroying the edge:

- reduces stop streaks;
- improves win rate;
- improves expectancy;
- reduces drawdown;
- reduces cluster risk;
- improves normalized pip outcome;
- improves daily stability;
- preserves enough signal count;
- improves robustness over many days.

## Final Boundary

Chapter 18 does not create constraints. It creates the statistical need to measure whether constraints should ever exist.
