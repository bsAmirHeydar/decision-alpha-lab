# Valid Hook View Filter — Start Here

This patch makes the production Hook view display only structurally valid Hook families:

1. **Hook After Opposing F3**
2. **Hook After Hook**

There is one visibility exception:

- When a valid Hook is the **second Hook in a Hook-after-Hook chain**, the first Hook is also displayed as the required parent companion.
- That first Hook is not promoted into a valid independent Hook. It is visible only because the second Hook cannot be read structurally without its immediate predecessor.

The patch is visualization/filtering focused. It does not change F logic, Rally logic, broker behavior, execution, risk sizing, or order sending.
