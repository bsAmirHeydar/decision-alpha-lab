# MQL5 Execution and Validation Layer

MQL5 is the project layer used for fast replay, MetaTrader-native execution, and Expert Advisor validation.

---

## Current role

MQL5 is no longer only an execution bridge. It is also the strictest environment for live-style validation because it can replay candle state and execution policies close to the platform that will trade the system.

---

## Official research rule

Main hypothesis Experts must not depend on completed samples for live validity.

For H0004 and H0005, the official direction is:

```text
Raw M0001 events
→ known-time batches
→ no fake same-time transitions
→ entry only after regime is known
→ measurement only after entry
```

---

## Debug vs main Experts

Debug Experts are allowed to test new contracts. Once a contract is accepted, it must be moved into the main Expert or a shared include used by the main Expert.

Accepted examples:

- D0010 proved H4 atomic no-sample regime batching.
- D0009 proved H5 atomic no-sample replay.
- Main H4/H5 should default to the atomic contract.

---

## Execution reporting rule

Every trading EA must distinguish:

- structural path metrics,
- execution metrics,
- realized R with real risk,
- floating MFE/MAE R,
- fixed reward hits,
- stop hits,
- forced exits,
- same-bar ambiguity.

---

## Compile discipline

After any MQL5 release:

1. apply the release,
2. sync include files if the installer provides this,
3. reopen MetaEditor,
4. compile changed Experts,
5. inspect warnings and errors,
6. commit only source/docs, never release archives.
