# Install — RTHP AI-Engine Input Binding

## Prerequisites

- Run from the repository root.
- The English RTHP Context and ACL-03 patches must already be committed.
- Canonical RTHP version must be `1.0.2`.
- Git working tree and staging area must be clean except for the downloaded ZIP.
- Python and pytest dependencies used by the repository must be available.

## Installation flow

1. Verify the release SHA-256 published with the ZIP.
2. Expand the ZIP at repository root.
3. Verify `RTHP_AI_INPUT_FILE_HASHES.sha256`.
4. Run smoke preflight; it must pass.
5. Run real-data preflight against the unresolved template; it must return the expected fail-closed blocker.
6. Run RTHP AI-input and regression tests.
7. Confirm Engine-invariance and canonical-Context-immutability reports are `PASS`.
8. Stage exactly the paths in `RTHP_AI_INPUT_FILE_INDEX.txt`.
9. Commit with `COMMIT_MESSAGE_RTHP_AI_INPUT.md` and push.

## Smoke preflight

```powershell
$env:PYTHONPATH = 'lab\11_strategy_factory\python'
python -m strategy_factory_rthp_context_v1.preflight `
  --source-jsonl 'lab\11_strategy_factory\generated_contexts\rthp_cross_symbol_cycle_divergence\ai_input\fixtures\rthp_ai_smoke_records.jsonl' `
  --output "$env:TEMP\rthp_ai_smoke_preflight.json"
```

## Test suites

```powershell
python -m pytest -q -p no:cacheprovider lab\11_strategy_factory\tests\rthp_ai_input
python -m pytest -q -p no:cacheprovider lab\11_strategy_factory\tests\rthp_context
python -m pytest -q -p no:cacheprovider lab\11_strategy_factory\tests\phase_uce_i16_context_onboarding
python -m pytest -q -p no:cacheprovider lab\11_strategy_factory\tests\phase_uce_i02_contexts
python -m pytest -q -p no:cacheprovider lab\11_strategy_factory\acl_os\tests_acl_02
python -m pytest -q -p no:cacheprovider lab\11_strategy_factory\acl_os\tests_acl_03
python -m pytest -q -p no:cacheprovider lab\11_strategy_factory\generated_contexts\rthp_cross_symbol_cycle_divergence\tests
```

## Real training

Do not replace unresolved binding fields with guessed values. Create a resolved binding artifact with immutable URIs and hashes, then run real preflight. A PASS is the prerequisite for submitting `train_activation.v1.json` to the existing ACL-05 batch builder.
