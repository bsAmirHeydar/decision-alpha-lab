# HOOK CANON STEP 5 — Closure Lifecycle and Strict Visible Set

This patch corrects two doctrine violations found on live MT5 screenshots:

1. valid-only rendering was still expanding selected valid Hooks into all same-origin sibling sequences;
2. visual terminal alignment was still allowed to follow raw price extremes instead of confirmed Hook terminal nodes.

The production rule is now strict:

- build all structural Hook candidates internally;
- reject/non-render candidates whose origin is touched before terminal-node confirmation;
- treat a Hook as closed only when its last same-side terminal node is confirmed;
- in valid-only view, draw only canonical valid Hook rows plus the explicit parent companion of a valid Hook-after-Hook child;
- never expand valid-only view to all same-origin structural siblings.

No trade execution, broker behavior, risk sizing, Zone logic, Rally logic, or F-counting canonical logic is changed.
