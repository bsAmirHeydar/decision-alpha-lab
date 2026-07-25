# VAL0011 — Main Atomic No-Sample Unification

## Purpose

Promote the atomic no-sample contracts from debug validators into the main H0004 and H0005 Experts.

---

## Motivation

A debug validator is useful, but the project should not keep correct logic only in debug files. If a debug contract is the right research contract, the main Expert must adopt it.

---

## Main changes

### H0004

The main H4 Expert should default to raw M0001 event known-time batches rather than completed M0002 branch sample sequences.

### H0005

The main H5 Expert should default to raw-event live-style replay rather than sample path reports.

Continuation R should default to explicit risk, preferably ATR risk, rather than implicit structural path denominators.

---

## Required sanity lines

H4:

```text
DAL_M0004_MAIN_ATOMIC_SANITY
DAL_D0010_AUDIT
```

H5:

```text
DAL_M0005_MAIN_ATOMIC_SANITY
DAL_D0009_AUDIT
```

---

## Legacy mode

Classic sample/path reports may remain available as opt-in legacy diagnostics, but they must not be the default source of live validity claims.
