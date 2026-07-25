# UC-03 Part 2 — Code, Context, Test and MQL5 Relocation

This delivery performs physical relocation only. It does not merge behavior, retire implementations, authorize trading, or authorize UC-04.

## Scope

- empty the legacy `lab/` production workspace;
- move Python packages to `src/engine/` under explicit legacy boundaries;
- move Context and experiment assets to `contexts/legacy/`;
- move tests and fixtures to `tests/legacy/`;
- move laboratory MQL5 and MQL5 test sources to standard MQL5 boundaries;
- move production-like packages out of `tools/` while retaining temporary namespace shims;
- rewrite active path consumers and depth-coupled repository-root discovery;
- issue the Part 3 handoff only after verification.

The `legacy` namespace is deliberate. Semantic ownership and duplicate implementation merge are UC-04 responsibilities.
