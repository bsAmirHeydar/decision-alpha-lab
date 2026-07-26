# CH15 — Statistical Reporting and Metric Language Doctrine

## 1. Purpose of this chapter

This chapter defines what the strategy must remember after a divergence becomes confirmed and tradeable.

The core idea is simple: the strategy is not evaluated by opinion. It is evaluated by repeated behavior across confirmed samples. Therefore the reporting layer must be rich enough to preserve all meaningful dimensions of each signal, but neutral enough not to turn untested assumptions into rules.

The strategy architect identified the key statistical families:

- win rate
- risk-to-reward
- profit or loss in pips / points
- profit or loss in pips divided by total daily market movement in pips
- cycle-group overlap
- signal count per day
- signal count per week
- signal count per month
- cycle-group type
- all other meaningful statistical fields discovered through the strategy doctrine so far

This means Chapter 15 is not only a performance report. It is a language of observation.

## 2. Confirmed, tradeable signals are the main sample

The main statistical population must include only signals that reached the confirmed and tradeable state.

A candidate is not enough.  
A raw hunt is not enough.  
A live intrabar difference between the symbols is not enough.  
A divergence that disappears before confirmation is not part of the main performance sample.

The signal enters the primary report only when:

1. a valid reference exists;
2. one symbol hunts the relevant reference;
3. the other symbol does not hunt its corresponding reference;
4. the active confirmation candle closes;
5. the divergence still exists at that close;
6. the signal becomes eligible for trade under the strategy rules.

This keeps the statistical field clean. The study is not about every possible visual event. It is about signals that the strategy itself would have allowed.

## 3. Non-actionable events are not required in the main report

The strategy architect answered that unconfirmed or non-actionable events do not need to be part of the main report at this stage.

This creates a clear boundary:

- primary report: confirmed, actionable, tradeable divergences;
- optional research archive: raw hunts, failed candidates, pre-confirmation events, visual ideas.

The base strategy report should not become overloaded with every incomplete market behavior. The first goal is to understand the edge of the valid signal, not every shadow around it.

Later, if needed, failed candidates can become a secondary research family. But they are not part of the primary Chapter 15 doctrine.

## 4. Cycle group type is mandatory

The type of cycle group must always be present in the report.

A signal without its cycle group is incomplete. Cycle-group identity is not a cosmetic label; it is one of the main statistical dimensions of the whole framework.

Each signal must remain connected to its CG family because later analysis may discover that:

- some CGs have better win rate;
- some CGs have worse stop behavior;
- some CGs create more movement but lower stability;
- some CGs work better inside cash session;
- some CGs work better outside cash session;
- some CGs are better for buy than sell;
- some CGs create better normalized movement against daily range;
- some CGs produce too many low-quality signals;
- some CGs become powerful only when overlapping with other CGs.

None of these are assumed now. But without mandatory CG tagging, none of them can be discovered later.

## 5. Win rate remains a primary health measure

From Chapter 14 and reinforced here, win rate is especially important because it shows how often signal families avoid stop-out.

The strategy is not only looking for large winners. It also wants to know which families repeatedly fail. A signal family may sometimes produce large movement, but if it creates too many stops, it may be psychologically and practically weaker.

Therefore win rate must be reported for every meaningful family:

- by cycle group;
- by direction;
- by hunter symbol;
- by clean symbol;
- by time window;
- by reference distance;
- by cash-session status;
- by overlap condition;
- by signal density condition;
- by week and month when enough samples exist.

Win rate does not replace expectancy. It is a health filter. It tells us whether a family survives contact with the stop.

## 6. Risk-to-reward remains a result lens

Risk-to-reward is a separate lens from win rate.

A signal family can have modest win rate but strong reward when correct. Another family can have high win rate but small result. Both are important.

The report should preserve at least these reward views:

- result at the end of the active cycle;
- maximum favorable reward after confirmation;
- maximum reward later in the same day;
- final day result if studied;
- realized R if a fixed exit is used;
- best available R inside defined later windows.

This keeps the strategy from becoming blind to movement potential.

## 7. Pip or point movement is a raw movement measure

The strategy architect named profit by pips as an important sample.

In index CFDs, depending on broker symbol naming, the language may be expressed as pip, point, or index movement. The conceptual meaning is the same: how far did the clean symbol move after the signal?

This movement should be studied in several ways:

- movement from entry to cycle-end exit;
- maximum favorable movement after entry;
- maximum adverse movement after entry;
- movement to the end of the day;
- movement before invalidation;
- movement during the next one, two, or several cycle windows.

Raw movement is important because dollar outcome can be affected by lot size and risk model. Pip or point movement preserves market behavior in its own terms.

## 8. Movement divided by total daily range is a new quality index

The user explicitly defined a valuable derived measure:

> profit in pips divided by total market movement in pips.

This is important because it normalizes signal movement against the size of the day.

A 40-point move on a small day may be meaningful. A 40-point move on a very large day may be ordinary. Raw movement alone does not show how much of the day's opportunity the signal captured.

The normalized movement index answers:

- Did the signal capture a meaningful portion of the day's movement?
- Was the movement large only in absolute terms, or also large relative to the day?
- Do some CGs capture a higher share of daily range?
- Do some time windows produce better normalized movement?
- Does cash session improve normalized movement?
- Does cycle-group overlap increase the share of day captured?

This index should become one of the signature statistical measures of EXP0017.

## 9. Cycle-group overlap matters

The user stated that cycle-group overlap is important.

Overlap means more than one CG family may produce a valid signal around the same market behavior. This does not automatically mean the signal is stronger. Previous chapters already established that CGs remain independent before testing.

But overlap is a valuable statistical field because later analysis may discover that overlap changes behavior.

Possible overlap conditions:

- same direction overlap: multiple CGs confirm buy or sell around the same area;
- mixed direction overlap: one CG signals buy while another signals sell;
- same clean-symbol overlap;
- different clean-symbol overlap;
- same reference-side overlap;
- overlapping confirmation windows;
- overlapping stop areas;
- overlapping time-target windows;
- overlap during cash session;
- overlap outside cash session.

In the base doctrine, overlap is not a reason to increase confidence. It is a field to be studied.

## 10. Signal frequency is part of strategy character

The number of signals per day, week, and month is important.

Frequency helps answer questions that win rate and reward cannot answer alone:

- Is this family too rare to trade consistently?
- Is this family too frequent and noisy?
- Does signal clustering predict poor outcomes?
- Does a high-signal day behave differently from a low-signal day?
- Does a CG become worse when it produces too many signals?
- Does the strategy produce enough samples for live evaluation?
- Does a month contain enough valid opportunities?

Frequency must be studied at several levels:

- total signals per day;
- signals per CG per day;
- buy signals per day;
- sell signals per day;
- signals per symbol role;
- signals per cash session;
- signals per week;
- signals per month;
- overlapping signals per day;
- conflicting signals per day.

## 11. Emotional language must be removed

The strategy architect explicitly said that emotional terms should be removed because an expert has no emotion.

This is an important language rule.

The report should not use terms such as:

- beautiful signal;
- ugly signal;
- scary signal;
- attractive signal;
- weak-looking signal;
- strong-looking signal without statistical definition;
- confident signal without score definition;
- clean in an emotional visual sense;
- risky by feeling;
- good by feeling.

The report should use measurable language:

- confirmed;
- invalidated;
- live;
- stopped;
- reached cycle-end target;
- maximum favorable movement;
- maximum adverse movement;
- realized R;
- dollar outcome;
- normalized movement;
- overlap count;
- signal frequency;
- win rate;
- expectancy;
- stop streak;
- sample count.

The expert should speak in measurable states, not emotions.

## 12. Recommended additional statistical fields

For questions where the strategy architect asked for recommendations, the following fields are recommended for later reports:

### 12.1 Signal identity

- trading day
- confirmation time in New York
- active cycle group
- active cycle index
- reference cycle index
- reference distance
- direction
- hunter symbol
- clean symbol
- reference side: high or low
- cash-session status

### 12.2 Validity state

- confirmed
- invalidated after confirmation
- invalidation time
- double-hunt condition
- still valid until exit

### 12.3 Trade result

- entry assumption
- stop distance
- realized result at cycle end
- dollar outcome
- R result
- pip or point result
- maximum favorable movement
- maximum adverse movement
- maximum same-day reward

### 12.4 Normalized movement

- daily range of clean symbol
- movement divided by daily range
- maximum favorable movement divided by daily range
- adverse movement divided by daily range

### 12.5 Frequency and clustering

- signal count per day
- signal count per week
- signal count per month
- same-direction overlap count
- opposite-direction overlap count
- overlapping CG count
- signal cluster density

### 12.6 Family classification

- CG family
- direction family
- symbol-role family
- reference-distance family
- time-window family
- overlap family
- invalidation family
- frequency family

These are not filters. They are report fields.

## 13. The report becomes the memory of the strategy

Previous chapters repeatedly refused to assume differences before testing. Chapter 15 creates the place where those differences can be discovered.

The report is therefore the strategy's memory.

It records what happened without emotion.  
It preserves every important identity of the signal.  
It keeps confirmed signals separate from unconfirmed noise.  
It allows CGs to remain independent.  
It allows future statistics to discover what matters.  
It prepares the ground for future model-building and AI scoring.

## 14. Final doctrine

A signal is not understood when it appears. It is understood after it is measured across enough confirmed samples.

Chapter 15 defines the measurement language of EXP0017.

The report must preserve:

- what the signal was;
- where it formed;
- which CG created it;
- which symbol hunted;
- which symbol stayed clean;
- when it confirmed;
- how it behaved after confirmation;
- how much it moved;
- how much it earned or lost;
- how much of the day it captured;
- whether it overlapped with other CGs;
- how often its family appears;
- whether its family survives statistical testing.

This is the bridge between strategy doctrine and statistical truth.
