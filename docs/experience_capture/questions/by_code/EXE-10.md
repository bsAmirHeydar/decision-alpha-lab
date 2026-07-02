# EXE-10 — Which execution templates do we need?

Section: Execution, Spread, Slippage, Pending Orders, and Order Management

### EXE-10 — Which execution templates do we need?

Why this matters: The answer determines the ExecutionIntent contract, execution simulator, and broker-safety gates.

Answer in these layers:
- Raw intuition: describe how you see it on the chart before formalizing it.
- Operational definition: explain how we could turn it into a field, rule, label, or policy.
- Exceptions: describe the cases where the rule fails, weakens, or changes meaning.
- Chart evidence: add examples when the idea is easier to understand visually.

Clarify these points:
- Define the cost thresholds that destroy optionality.
- Explain pending-order lifecycle: place, keep, cancel, replace, expire.
- Separate structural stop from broker stop if needed.
- Define market-entry permission if any.
- Explain what should happen when spread, phase, destination, or anchor validity changes.

Future system outputs affected by this answer:
- execution cost fields
- pending order state
- cancel policy
- replace policy
- ExecutionIntent fields
- risk profile placeholders

Image guidance: A chart example is useful if order movement, cancel, or replace is easier to see visually.

Recommended answer folder: ../answers/EXE-10/

User answer:

