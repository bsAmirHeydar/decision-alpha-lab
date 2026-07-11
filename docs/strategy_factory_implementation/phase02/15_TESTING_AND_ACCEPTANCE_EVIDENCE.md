# Testing and Acceptance Evidence

## Python Tests

- Runtime config validation.
- Legal and illegal state transitions.
- FIFO and sequence behavior.
- Both bus overflow modes.
- Required package layout.
- Dependency boundary scan.
- Thin Host scan.
- No live order authority.
- Port inventory.
- Roadmap and phase status.

## MQL5 Self-Test

The self-test constructs fixture clock, anatomy, feature and sink services. One tick produces one canonical event and one snapshot. It also validates the state machine, typed bus and explicit no-send boundary.

## Environment Limitation

MetaEditor is not available in the build environment. Static validation and Python tests are complete. Local MetaEditor compilation and tester execution remain required acceptance evidence.
