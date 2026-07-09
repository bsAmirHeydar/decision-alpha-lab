# No Structural Fallback In Production

## Policy

Valid-only production view must not fall back to structural Hook candidates.

```text
No valid Hook => draw nothing
```

Fallback can be useful for debugging, but it must require an explicit debug input and must not be active in production valid-only mode.
