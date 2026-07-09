# Beta QA Release Gate

A beta release is allowed only after these gates are checked:

- compile gate
- source bridge gate
- time normalization gate
- visual gate
- filter gate
- alert gate
- packaging gate

The canonical checklist is:

```text
release/customer_docs/BETA_QA_CHECKLIST.md
```

## Beta failure policy

If any gate fails, do not sell the product as stable. Continue as internal beta or paid beta with explicit limitations.
