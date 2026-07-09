# CH20 — Strategy Version Governance and Non-Mutation Doctrine

## 1. Purpose of this chapter

Chapter 20 defines how the strategy may evolve without losing its identity.

The previous chapters built a very clear base layer:

- two-symbol intermarket divergence;
- touch-only hunt;
- candle-close confirmation;
- clean-symbol execution;
- same-day reference field;
- independent cycle groups;
- independent cycles inside each CG;
- no pretest hierarchy;
- no emotional or visual filtering;
- statistical reporting from confirmed tradeable signals;
- model as analyst, ranker, comparer, and statistical observer.

Chapter 20 protects that base layer from premature optimization.

The most important rule is this:

> In the current version, the model does not change the strategy. It only tests, measures, compares, ranks, and reports.

This is not a small technical detail. It is a strategic governance rule.

## 2. Repeated questions should return to existing doctrine

The strategy architect answered that the first question had already been answered and was mostly repetitive.

This creates a useful documentation principle:

When a future question is only a repetition of a doctrine already locked in earlier chapters, the system should not create a new conflicting rule. It should point back to the original doctrine.

Examples:

- if the question asks again whether CGs are independent, the answer is Chapter 11 and Chapter 12;
- if the question asks again whether the model changes the strategy, the answer is Chapter 16, Chapter 17, and Chapter 20;
- if the question asks again whether all signals are preserved until invalidation, the answer is Chapter 12;
- if the question asks again whether statistics can rank families, the answer is Chapter 14, Chapter 15, and Chapter 16;
- if the question asks again whether future optimization is possible, the answer is Chapter 20.

This prevents doctrine drift.

## 3. Current version: no strategy mutation

The current version is statistical only.

It may:

- count signals;
- measure win rate;
- measure stop rate;
- measure stop streaks;
- measure risk-to-reward;
- measure pip movement;
- measure dollar outcome;
- measure normalized movement relative to daily range;
- compare cycle groups;
- compare directions;
- compare hunter and clean symbols;
- compare time windows;
- compare CG overlaps;
- rank families;
- identify weak families;
- identify promising families;
- report complexity;
- suggest future tests.

It may not:

- change cycle groups;
- remove cycle groups;
- add new entry conditions;
- remove entry conditions;
- alter the candle-close confirmation rule;
- alter the hunt definition;
- alter the clean-symbol doctrine;
- change the time target;
- change the daily trading window;
- block signals;
- change risk;
- change stop logic;
- choose live trades by itself;
- transform statistics into strategy rules without human approval.

The model is allowed to describe. It is not allowed to mutate.

## 4. Future versions may optimize the strategy

The strategy architect allowed the possibility that future versions may optimize the strategy and create changes inside it.

This is not active now.

It is a future gate.

The future optimizer may one day examine:

- whether some CGs should be disabled;
- whether some CGs should receive lower or higher weight;
- whether CG overlap should create stronger or weaker permission;
- whether some time windows should be preferred;
- whether the cycle-end target should be modified;
- whether a maximum intraday reward exit is better;
- whether some stop sizes should be avoided;
- whether late entries damage expectancy;
- whether position clusters need exposure limits;
- whether hedging creates or destroys value;
- whether the clean-symbol doctrine needs exceptions.

But these possibilities belong to a later version. They are not current rules.

## 5. The strategy architect decides after statistics

The strategy architect said that after statistics are collected, he will decide what should be done.

This locks the authority structure:

1. The strategy creates raw confirmed signals.
2. The report preserves those signals.
3. The model analyzes the signals.
4. The model ranks and compares families.
5. The model may recommend changes.
6. The strategy architect reviews the evidence.
7. Only the strategy architect decides whether a recommendation becomes a rule.

This creates a human-governed research loop.

The model is powerful, but it is not sovereign.

## 6. Unknown recommendations must not change the strategy

Several answers in this chapter use the phrase: "I do not know, use your recommendation, but the strategy must not change."

This is important.

It means recommended analysis is allowed. Recommended documentation is allowed. Recommended reporting fields are allowed. Recommended future research maps are allowed.

But recommended strategy changes are not allowed in the current version.

A recommendation can become one of three things:

- an extra field in the report;
- a future hypothesis;
- a future version proposal.

It cannot become an immediate rule.

## 7. CG overlap may make the model complex

The strategy architect identified CG overlap as a likely source of model complexity.

This is a central warning.

CG overlap can create cases such as:

- multiple CGs confirming the same direction close together;
- multiple CGs confirming opposite directions close together;
- one symbol clean in one CG and hunter in another CG;
- one reference used in multiple CG contexts;
- signal clusters across small and large CGs;
- simultaneous tradeable signals with different time targets;
- overlapping exits;
- overlapping stops;
- hedged positions created by independent CG families;
- multiple outcomes attached to one market moment.

The base doctrine says these signals remain independent. But the model may need a sophisticated report layer to compare them.

This is not a reason to remove overlap now. It is a reason to track overlap carefully.

## 8. Future decisions are intentionally postponed

The answer to Question 10 was that the strategy architect will define it later.

This should not be filled with speculation.

Some decisions must remain open until the base research is complete. These may include:

- what optimization authority the model may later receive;
- whether future AI can propose rule changes;
- how CG overlap should be scored;
- whether position limits should be introduced;
- whether some CGs should be disabled;
- whether filters should be created;
- whether live model scoring should be allowed;
- whether strategy variants should split into separate profiles;
- whether the model should become adaptive in later versions.

The current answer is: not now.

## 9. Chapter 20 doctrine statement

The current version of EXP0017 is a statistical research and reporting framework for the fixed base strategy. It may analyze, rank, compare, and recommend, but it must not mutate the strategy. Future versions may introduce optimization, but only after the base statistics are collected and the strategy architect explicitly decides what should change.
