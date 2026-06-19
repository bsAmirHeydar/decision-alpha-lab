# MQL-Native Migration Decision

## Summary

The Decision Alpha Lab project will migrate M0001 from a Python-brain / MQL-visual bridge architecture to a native MQL5 execution architecture.

The previous Python implementation is preserved as an archived reference in the branch:

```text
archive/python-brain-m0001
```

Going forward, MQL5 will become the primary runtime for live logic, visual validation, strategy testing, and research iteration.

## Why Python Is Being Removed From the Active Runtime

The Python bridge achieved an important goal: it proved the core M0001 idea, clarified the event model, and produced a useful reference implementation. However, it introduced runtime problems that are unacceptable for this project’s current direction.

The main issues were:

1. **Asynchronous execution lag**

   MT5 Strategy Tester advances through simulated market time, while Python runs outside the terminal. Even with aggressive polling, the bridge can create timing lag between candle availability, Python computation, and visual redraw.

2. **File-locking and adapter friction**

   The bridge depends on shared files between MQL and Python. This creates operational issues such as file locks, temporary read/write conflicts, retry logic, and fragile CSV adapter behavior.

3. **Live-semantics ambiguity**

   The project requires exact live logic: the same data available at the same simulated moment must produce the same decision and visual state. A separate Python process makes this harder to guarantee and harder to debug visually.

4. **Overhead during rapid hypothesis testing**

   The project needs fast iteration. MQL5 provides immediate access to chart data, Strategy Tester state, visual objects, and execution events. Keeping Python in the loop slows the feedback cycle.

5. **Single-runtime simplicity**

   M0001 is not only a research metric; it is a live-market decision component. For this phase, the safest architecture is to keep detection, metric logic, event state, visual validation, and tester behavior inside one runtime: MQL5.

## What Is Not Being Removed

The research structure stays.

The project will keep the same scientific workflow:

```text
observation
hypothesis
experiment
validation
visual audit
archive
```

The migration removes Python from the active runtime, not the research discipline.

The following ideas remain central:

* explicit hypothesis tracking
* structural node definitions
* reproducible parameter sets
* visual validation journals
* pass/fail audit cases
* live-safe decision semantics
* clear separation between research concept and production signal

## New Direction

MQL5 becomes the source of truth for M0001.

The target architecture is:

```text
MQL5 chart/tester data
        ↓
MQL5 structural node engine
        ↓
MQL5 M0001 RTV/event engine
        ↓
MQL5 visual audit layer
        ↓
MQL5 strategy/test execution
```

No external Python watcher is required.

No CSV bridge is required for live logic.

No Parquet artifact is required for the execution loop.

Research documentation may still export reports or screenshots, but the active strategy logic lives inside MQL5.

## Archived Reference

The Python implementation is not deleted historically. It is frozen in:

```text
archive/python-brain-m0001
```

That branch exists for comparison, reference, and possible future offline analysis.

The active development branch will move toward:

```text
mql-native-migration
```

## Decision

Python is removed from the active M0001 runtime because it adds latency, synchronization risk, file I/O friction, and live-semantics ambiguity.

MQL5 is selected as the active runtime because it gives direct access to the market stream, chart state, tester timeline, visual objects, and execution environment in one place.

This aligns the project with its real objective:

```text
fast, live-safe, visually auditable quantitative decision research
```
