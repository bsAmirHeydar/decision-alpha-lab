# Strategy Factory Phase 01 — MQL5-First Contracts and Schema

This additive patch implements the canonical contract foundation for the Strategy Factory. MQL5 is the primary runtime implementation. Python is a strict research mirror.

Start with:

`docs/strategy_factory_implementation/phase01/00_PHASE_01_MOC.md`

Run Python/static checks with:

`powershell -ExecutionPolicy Bypass -File tools/strategy_factory/run_phase01_tests.ps1`

Compile the MQL5 self-test on Windows with:

`powershell -ExecutionPolicy Bypass -File tools/strategy_factory/compile_sf01_contracts.ps1 -MetaEditorPath "C:\...\MetaEditor64.exe"`
