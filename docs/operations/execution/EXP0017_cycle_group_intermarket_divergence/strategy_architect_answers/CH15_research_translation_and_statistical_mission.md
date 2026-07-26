# CH15 — Research Translation and Statistical Mission

## Research mission

Chapter 15 translates the strategy architect's answers into the statistical mission of the reporting layer.

The mission is to build a clean sample of confirmed and tradeable divergences, then measure them from multiple independent angles without adding emotional labels or premature filters.

## Primary sample boundary

The primary sample includes only confirmed signals that reached trade permission.

A valid sample requires:

- confirmed divergence;
- candle close completed;
- no double-hunt invalidation before confirmation;
- clean symbol still holds its reference at confirmation;
- signal belongs to the current trading day;
- signal belongs to a known cycle group;
- signal is eligible for the base trade model.

Events outside this state can be archived later, but they are not part of the primary performance population.

## Core statistical families

### 1. Win-rate family

Win rate must be studied by:

- all signals;
- each CG;
- buy versus sell;
- SPX clean versus NDX clean;
- SPX hunter versus NDX hunter;
- cash session versus outside cash;
- reference distance;
- overlap condition;
- signal frequency condition;
- day, week, and month.

The goal is to discover which families avoid stop-out better.

### 2. Reward family

Reward must be studied as:

- realized R;
- risk-to-reward at cycle end;
- maximum favorable R;
- maximum same-day R;
- R before invalidation;
- R after several future windows.

The goal is to discover movement potential, not only final win/loss.

### 3. Pip / point movement family

The report should track raw movement in market units:

- movement from entry to cycle end;
- movement from entry to maximum favorable point;
- movement from entry to maximum adverse point;
- movement from entry to day end;
- movement during later windows.

The goal is to separate market movement from money management.

### 4. Daily-range-normalized family

The report should compute movement relative to the full daily range.

Important questions:

- What percentage of daily range did the signal capture?
- Does a signal capture more of the day in some CGs?
- Does cash session produce better normalized movement?
- Does CG overlap improve normalized movement?
- Do buy and sell divergences differ in normalized capture?

This measure is important because it turns raw movement into contextual movement.

### 5. Frequency family

The report must study density:

- signals per day;
- signals per week;
- signals per month;
- signals per CG per day;
- overlapping signals per day;
- conflicting signals per day;
- signal clusters before stop streaks;
- quiet days versus dense days.

The goal is to understand opportunity rate and noise pressure.

### 6. Overlap family

Cycle-group overlap should be preserved as a study field.

Possible overlap questions:

- Do same-direction overlaps improve win rate?
- Do opposite-direction overlaps reduce win rate?
- Does overlap increase movement potential?
- Does overlap increase stop risk?
- Does overlap work differently in cash session?
- Does overlap matter only for certain CG families?

No answer is assumed. The field must be recorded.

## Recommended report layers

### Layer 1 — Base performance

- total sample count;
- win rate;
- stop rate;
- average R;
- median R;
- expectancy;
- average dollar outcome;
- total dollar outcome;
- best and worst sequence.

### Layer 2 — Cycle-group view

- sample count per CG;
- win rate per CG;
- expectancy per CG;
- stop streak per CG;
- movement per CG;
- normalized movement per CG;
- signal frequency per CG.

### Layer 3 — Direction view

- buy sample count;
- sell sample count;
- buy win rate;
- sell win rate;
- buy expectancy;
- sell expectancy;
- buy/sell movement profile.

### Layer 4 — Symbol-role view

- SPX hunter / NDX clean;
- NDX hunter / SPX clean;
- SPX clean performance;
- NDX clean performance;
- hunter-role outcomes;
- clean-role outcomes.

### Layer 5 — Time view

- 09:30 to 16:00 New York;
- outside cash session;
- early cash session if later needed;
- late cash session if later needed;
- high-frequency days;
- low-frequency days.

### Layer 6 — Overlap view

- no overlap;
- same-direction overlap;
- opposite-direction overlap;
- multiple-CG overlap;
- overlap at confirmation;
- overlap after confirmation;
- overlap plus high stop-pressure condition.

## Recommended analytical additions

The strategy architect allowed additional useful statistical ideas. The following are recommended:

1. **Maximum favorable excursion** — how far price moved in favor of the signal before exit or day end.
2. **Maximum adverse excursion** — how much pain the signal created before working or failing.
3. **Time to first favorable movement** — how quickly the signal starts working.
4. **Time to stop** — whether bad signals fail quickly or slowly.
5. **Time to maximum reward** — whether the signal reaches best reward before or after cycle end.
6. **Giveback after maximum reward** — whether cycle-end exit loses much of the potential move.
7. **Signal density rank** — whether a day is normal, crowded, or quiet by signal count.
8. **Overlap count** — number of CGs giving related signals near the same market area.
9. **Conflict count** — number of valid signals pointing opposite directions in the same area or window.
10. **Normalized adverse movement** — adverse move divided by daily range.

These fields support future model-building without becoming immediate filters.

## Report language rule

Reports must avoid emotional language.

Instead of saying:

- good signal;
- bad signal;
- beautiful setup;
- scary drawdown;
- strong-looking move;

Use:

- profitable signal;
- stopped signal;
- high normalized movement;
- high adverse movement;
- low win-rate family;
- positive expectancy family;
- high overlap condition;
- high signal-density day.

## Final research mission

The statistical report must let the strategy discover its own hierarchy.

The model begins with equality:

- all CGs valid;
- both directions valid;
- both symbols valid;
- all confirmed signals valid;
- all timing windows valid;
- all reference distances descriptive only;
- all overlaps descriptive only.

Then the report measures. After enough data, the strategy can decide.
