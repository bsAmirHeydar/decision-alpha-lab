# Strategy Factory V2 MQL5 Runtime

This directory contains the compiled-side contracts for a bounded context-to-decision path. It intentionally contains no `OrderSend`, `OrderCheck`, or `CTrade` authority. Live execution remains behind the repository's broker, risk, lifecycle, and promotion gates.

Core files:

- `SF2_Contracts.mqh` — canonical event, feature, candidate, score, and decision structures.
- `SF2_ContextFrame.mqh` — immutable-at-decision feature frame.
- `SF2_PluginInterfaces.mqh` — anatomy-independent provider/model/builder interfaces.
- `SF2_DecisionPlan.mqh` — startup-compiled thresholds and latency budgets.
- `SF2_FastDecisionEngine.mqh` — deterministic candidate selection and abstention.
- `SF2_LatencyBudget.mqh` — microsecond stage timing.
- `SF2_Telemetry.mqh` — bounded non-authoritative decision telemetry.
- `SF2_RuntimeGate.mqh` — kill switch, model readiness, context readiness, and paper-mode gate.

The intended production topology is:

`Existing anatomy engine -> SF2_ContextFrame -> bounded candidate builders -> local model -> SF2_FastDecisionEngine -> existing hard risk gate -> existing paper/broker adapter`.
