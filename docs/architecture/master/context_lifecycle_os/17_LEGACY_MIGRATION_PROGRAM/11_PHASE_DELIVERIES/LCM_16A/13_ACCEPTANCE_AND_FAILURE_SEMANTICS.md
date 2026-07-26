# Acceptance and failure semantics

`PASS` means the named evidence exists and validates. `FAILED` means a deterministic requirement failed. `BLOCKED` means a required prerequisite or environment is unavailable. `UNKNOWN` means evidence supports neither PASS nor FAIL. `PARTIAL` means evidence exists but acceptance is incomplete.

The current package validation is PASS; the closure decision is BLOCKED by external MetaEditor, Strategy Tester and external-consumer evidence, plus Git LFS materialization in the supplied source archive.
