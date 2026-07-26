# CH18 — Research Translation and Statistical Mission

## Research Purpose

Chapter 18 creates the unrestricted execution sample. This sample is necessary because the strategy architect wants to discover, not assume, whether trade limits, position caps, hedge restrictions, repeated-entry filters, or post-loss rules are beneficial.

The research mission is to observe every confirmed and non-invalidated divergence as a tradeable sample.

---

## Primary Research Questions

### 1. Does no-limit execution produce acceptable expectancy?

The raw model allows all valid signals. The first question is whether the unrestricted field itself has positive or acceptable behavior.

Metrics:

- win rate;
- stop rate;
- expectancy;
- dollar outcome;
- R outcome;
- pip outcome;
- normalized pip outcome;
- maximum drawdown by open cluster;
- consecutive loss count;
- daily worst loss;
- weekly worst loss.

### 2. Does same-CG repetition help or hurt?

Because multiple positions from one CG are allowed, each same-CG repetition must be studied.

Examples:

- first signal from CG that day;
- second signal from same CG;
- third signal from same CG;
- multiple signals in same cycle;
- repeated signals across later cycles;
- signals after a stop-out;
- signals after a win.

Possible findings:

- first signal is best;
- repeated signals are better;
- after-loss signals are weak;
- after-loss signals are strong;
- same-CG clustering creates risk;
- same-CG clustering creates edge.

None of these are assumed now.

### 3. Does hedge permission improve or damage results?

The base layer allows hedging. The research must measure:

- hedged signal frequency;
- hedged signal win rate;
- hedged signal expectancy;
- buy leg versus sell leg results;
- CG that dominated conflicts;
- symbol-role that dominated conflicts;
- whether holding both is better than choosing one;
- whether future conflict ranking is needed.

### 4. Does no position limit create unacceptable exposure?

The base model has no limit. The research model must still measure exposure risk.

Fields:

- open positions at signal time;
- open positions after entry;
- number of positions from same CG;
- number of positions from same symbol;
- number of positions in same direction;
- number of opposite-direction positions;
- total open risk;
- total open R exposure;
- cluster drawdown;
- cluster recovery;
- daily position density.

### 5. Does immediate entry after confirmation remain optimal?

Immediate entry is the base rule. Future analysis can compare it against possible alternatives without changing the base doctrine.

Potential comparison ideas:

- immediate entry;
- next-candle delayed entry;
- pullback entry;
- midpoint entry;
- retest entry;
- no-delay versus delayed result.

But the main sample remains immediate entry.

---

## Required Statistical Families

Every execution event should be classifiable by:

- CG type;
- current cycle number;
- reference cycle distance;
- hunter symbol;
- clean symbol;
- direction;
- cash-session status;
- number of active positions;
- same-CG open position count;
- same-symbol open position count;
- same-direction open position count;
- opposite-direction open position count;
- whether hedged exposure exists;
- whether this is first, second, third, or later signal from that CG that day;
- whether prior same-CG signal won or lost;
- whether prior same-symbol signal won or lost;
- whether prior opposite-direction signal exists;
- whether signal is part of a cluster.

---

## Position Cluster Study

Chapter 18 makes position cluster analysis essential.

A position cluster is a group of open trades that coexist during overlapping time.

Cluster dimensions:

- cluster size;
- cluster direction mix;
- cluster CG mix;
- cluster symbol mix;
- cluster start time;
- cluster duration;
- cluster maximum favorable outcome;
- cluster maximum adverse outcome;
- cluster final outcome;
- cluster stop count;
- cluster recovery behavior.

### Why this matters

No-limit execution can be profitable per signal but dangerous at portfolio level. Chapter 18 does not impose limits, but it demands measurement of the risk created by no limits.

---

## Future Constraint Discovery

The research layer should later answer whether any of these restrictions improve the strategy:

- max total open positions;
- max positions per CG;
- max positions per symbol;
- max positions per direction;
- max same-CG signals per day;
- post-loss cooldown;
- stop-streak defense;
- hedge ban;
- hedge reduction;
- conflict ranking;
- CG priority;
- time-window execution caps;
- daily loss stop;
- weekly exposure cap.

These are not base rules. They are post-statistical candidates.

## Final Research Mission

Chapter 18's mission is to preserve the full unrestricted execution universe first, then let data decide whether execution constraints should exist.
