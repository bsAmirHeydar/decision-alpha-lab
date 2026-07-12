# NDS F2 Waist-Break Point-2 Limit Setup

## Status

Canonical execution contract for the dedicated lightweight Strategy Tester profile.

## Core sentence

After a complete two-leg F2 flag exists, the F2 waist is treated as structural Point 1. A strict penetration beyond that waist is Point 2. The system stages a limit order strictly beyond the F2 waist so the fill is the executable Point 2, places the stop beyond the direct parent F1 waist, and targets the F2 Leg2 endpoint—the end of the two-leg F2 flag.

## Index

1. [Canonical setup contract](01_canonical_setup_contract.md)
2. [Structural anatomy](02_structural_anatomy.md)
3. [Execution state machine](03_execution_state_machine.md)
4. [Price and order semantics](04_price_and_order_semantics.md)
5. [Lifecycle and edge cases](05_lifecycle_and_edge_cases.md)
6. [Module architecture](06_module_architecture.md)
7. [Validation and acceptance](07_validation_and_acceptance.md)
8. [Operator guide](08_operator_guide.md)
9. [Correction of the previous implementation](09_previous_implementation_correction.md)
