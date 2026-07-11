---
type: strategy-factory-reference
status: canonical
title: "Maximum Alpha Extraction and Exploitation Playbook"
tags:
  - strategy-factory
  - alpha-extraction
  - portfolio
  - reference
---

# Maximum Alpha Extraction and Exploitation Playbook

## Objective

The Strategy Factory should extract every defensible economic use from a mature anatomy while preventing the search itself from manufacturing alpha. The process is broad in discovery, narrow in confirmation, and conservative in capital.

## Information-use matrix

For each anatomy, test whether it adds value as:

| Role | Question |
|---|---|
| Direction | Which side has positive conditional expectancy? |
| Timing | When should an existing strategy activate or stop? |
| Location | Where can risk be made small relative to potential? |
| Filter | Which events should be skipped? |
| Regime | Which execution family is appropriate now? |
| Stop | What price/time invalidates the thesis? |
| Exit | When does the anatomy's information expire? |
| Sizing tier | Does it identify safer opportunity, subject to hard caps? |
| Veto | Does it prevent trades from another strategy? |
| Portfolio | Does it signal correlated exposure or hedge need? |

An anatomy may fail as a standalone entry but succeed as an exit or no-trade filter. Those are distinct hypotheses and trials.

## Directional hypothesis set

Where coherent, test:

- reversal after the event;
- continuation after confirmation;
- leader/lagger catch-up;
- failed-signal continuation;
- volatility expansion without directional prediction;
- compression or no-trade state;
- cross-sectional relative value.

Do not force every anatomy into all roles. The doctrine and mechanism determine which are admissible.

## Execution geometry set

Use a small library of orthogonal entries, stops, and exits. The first matrix should identify where value resides:

```text
entry: immediate vs pullback/location
stop: exact anatomy vs volatility buffer
exit: fixed R vs structural/time
```

Only after one dimension demonstrates value should it be refined. Dense parameter optimization is delayed and nested.

## Statistical extraction

For each hypothesis:

1. calculate unconditional and matched base rates;
2. measure fill and net execution outcomes;
3. attribute by causal context;
4. estimate cluster/block uncertainty;
5. test incremental uplift;
6. apply multiple-testing and selection-aware controls;
7. stress costs, delay, fills, parameters, tails, feeds, and regimes;
8. freeze and confirm.

A positive bucket is not promoted until it survives this sequence.

## AI extraction

AI is applied in escalating stages:

1. rule baseline;
2. trade/skip meta-label;
3. expected-R prediction;
4. candidate ranking;
5. calibrated policy decision;
6. sequence model if justified;
7. contextual bandit only after live feedback infrastructure.

Use active learning to send uncertain or novel cases to your review. Capture your reasoning as structured, timestamped labels. Compare human, rule, and model decisions rather than assuming any is truth.

## Portfolio extraction

Once several strategy versions are validated, combine them through event-cluster exposure. Measure overlap and marginal portfolio contribution. A strategy with moderate standalone performance may be valuable if independent; a high-return duplicate may add no capital value.

Portfolio candidate selection should account for:

- expected return and lower bound;
- drawdown and tail loss;
- dependence and conflict;
- capacity and costs;
- event frequency;
- operational reliability;
- model/calibration uncertainty.

## Speed strategy

The fastest valid implementation order is:

```text
1 anatomy adapter
-> 1 bounded candidate matrix
-> 1 outcome dataset
-> standard statistical/anti-overfit pack
-> fixed setup baseline
-> first meta-label/ranker
-> paper bridge
```

Then add anatomies in parallel as plugins. Do not build a universal UI, complex RL system, or ultimate multi-anatomy model before the first pipeline closes to paper.

## Scaling doctrine

Research breadth can be explosive; capital promotion must be rare. Use:

```text
Build many
Test independently
Kill aggressively
Confirm narrowly
Paper faithfully
Micro-live cautiously
Scale only after proof
```

Scale depends on live execution fidelity and portfolio capacity, not backtest confidence. Risk increases through predeclared tiers and can be reduced immediately by hard gates.

## Kill discipline

Every strategy declares conditions that end or simplify it. Examples:

- no uplift over matched baseline;
- cluster lower bound remains negative;
- effect vanishes after costs or one-bar delay;
- PBO/selection tests indicate unstable winner selection;
- definition cannot be reproduced mechanically;
- cross-feed result reveals artifact;
- paper/live event or cost mismatch persists;
- portfolio marginal contribution is nonpositive.

Killing a version is productive because the shared factory, data, policies, and lessons remain. The platform becomes faster by preserving negative knowledge.

## Final operating model

Your unique value is the anatomy and the ability to formalize it rapidly. The factory converts that value into a standardized portfolio of falsifiable execution hypotheses. AI searches conditional structure; deterministic systems execute; risk gates protect capital. This division allows maximum exploitation without sacrificing your market language or giving model outputs uncontrolled authority.
