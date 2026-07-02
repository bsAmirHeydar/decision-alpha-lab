# Execution, Spread, Slippage, Pending Orders, and Order Management

This section defines execution reality: spread, slippage, pending orders, cancel, replace, and risk profile.

How to answer this section:
- Answer in your own words first; do not force a clean definition too early.
- Add rules, exceptions, and chart examples separately.
- Use the question code in every image caption or filename.
- If something is still intuitive and not formal, say so clearly.

Questions:

### EXE-01 — What is the maximum acceptable spread-to-risk ratio?

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

Recommended answer folder: ../answers/EXE-01/

User answer:


### EXE-02 — Should spread be calculated in the entry itself or only in validation?

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

Recommended answer folder: ../answers/EXE-02/

User answer:


### EXE-03 — Should commission and slippage be included now or later?

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

Recommended answer folder: ../answers/EXE-03/

User answer:


### EXE-04 — When should a pending limit be cancelled?

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

Recommended answer folder: ../answers/EXE-04/

User answer:


### EXE-05 — When should a pending limit be replaced?

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

Recommended answer folder: ../answers/EXE-05/

User answer:


### EXE-06 — If price comes near entry but does not fill and structure changes, what happens to the order?

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

Recommended answer folder: ../answers/EXE-06/

User answer:


### EXE-07 — If Y-phase changes, should all previous pending orders be cancelled?

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

Recommended answer folder: ../answers/EXE-07/

User answer:


### EXE-08 — If entry is filled and then destination changes, what do you do?

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

Recommended answer folder: ../answers/EXE-08/

User answer:


### EXE-09 — If spread suddenly widens, should the pending order be removed or only new trades blocked?

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

Recommended answer folder: ../answers/EXE-09/

User answer:


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


### EXE-11 — In which conditions is market entry allowed?

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

Recommended answer folder: ../answers/EXE-11/

User answer:


### EXE-12 — Should broker stop and structural stop be separate?

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

Recommended answer folder: ../answers/EXE-12/

User answer:


### EXE-13 — How should order sizing and risk profile be introduced later?

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

Recommended answer folder: ../answers/EXE-13/

User answer:

