---
title: RTHP Feature Binding IR
status: compiled
version: 1.0.2
---
# Feature Binding IR

- Feature IR digest: `sha256:61ed49e77e9e793e4a4e8849cbae55299a86c2c3d625208ac4199ac6ebd01b69`
- Feature order frozen: `true`
- Fusion policy: `Join only by registered symbol-pair identity, family scope, cycle identities, and equal synchronized confirmation-close identity.`
- Missing-view policy: `MASK_AND_ABSTAIN`

## Bound views

- `RTHP_EVENT_VIEW` — kind `EVENT_STREAM`, runtime order `0`, known-time safe `true`
- `RTHP_REFERENCE_STATE_VIEW` — kind `TABULAR`, runtime order `1`, known-time safe `true`

The compiler binds only declared Context facts and state. It does not create labels, outcomes, predictions, expected returns, entry features, or treatment-selection features.
