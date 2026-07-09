# Presets and Default Builds

## Presets

| Preset | Purpose |
|---|---|
| `gartal_terminal_beta_sample.set` | visual QA without live source |
| `gartal_terminal_live_bridge.set` | beta live-source workflow |
| `gartal_terminal_stable_customer.set` | strict customer build profile |

## Default philosophy

Beta builds are forgiving. Stable builds are strict.

- Beta can fall back to sample data.
- Stable should not silently fall back to sample data.
- Stable hides debug noise.
- Stable requires licensing when configured.
