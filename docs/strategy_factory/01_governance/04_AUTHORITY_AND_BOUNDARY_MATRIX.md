---
type: strategy-factory-document
status: canonical
title: "Authority and Boundary Matrix"
tags:
  - strategy-factory
---

# Authority and Boundary Matrix

The factory treats authority as a scarce capability. Every component has explicit permissions and prohibitions.

## Authority matrix

| Component | May define anatomy | May create candidates | May score | May size risk | May send order |
|---|---:|---:|---:|---:|---:|
| Anatomy adapter | Yes, from approved canon | No | No | No | No |
| Candidate engine | No | Yes | No | No | No |
| Statistical engine | No | No | Evaluate only | No | No |
| ML model | No | Rank/score existing candidates | Yes | Suggest tier only | No |
| Risk gate | No | No | No | Enforce limits | No |
| Broker bridge | No | No | No | No | Yes, only approved intent |
| LLM | Draft/audit under review | Propose policies | Explain | No | Never |

## Hard boundary violations

Examples include calculating a feature with the completed day's range, selecting a stop after seeing MAE, allowing a model to choose a policy never declared in the manifest, updating training weights from live outcomes inside the EA, or sending an order before a risk reservation exists. These are architecture failures, not minor bugs.

## Human authority

The architect owns doctrine and promotion. Human approval does not excuse leakage or bypass hard risk limits. Conversely, automated evidence cannot promote itself. The system records who approved each semantic version and which unresolved risks were accepted.

