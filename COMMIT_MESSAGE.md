```powershell
git add -- `
  "mql5/Include/AlphaLab/StrategyFactory/Contracts" `
  "mql5/Experts/StrategyFactoryTests/SF01_ContractSelfTest.mq5" `
  "lab/11_strategy_factory/python/strategy_factory_contracts" `
  "lab/11_strategy_factory/schemas/v1" `
  "lab/11_strategy_factory/test_vectors/v1" `
  "lab/11_strategy_factory/tests/phase01_contracts" `
  "lab/11_strategy_factory/implementation_program/phase_status/PHASE_01.json" `
  "lab/11_strategy_factory/implementation_program/phase_status/PHASE_01_HANDOFF_TO_PHASE_02.json" `
  "docs/strategy_factory_implementation/phase01" `
  "docs/obsidian_deep/00_mocs/STRATEGY_FACTORY_PHASE01_MQL5_FIRST_CONTRACTS_MOC.md" `
  "tools/strategy_factory" `
  "README_STRATEGY_FACTORY_PHASE01_IMPLEMENTATION.md" `
  "INSTALL_STRATEGY_FACTORY_PHASE01_IMPLEMENTATION.md" `
  "STRATEGY_FACTORY_PHASE01_PATCH_MANIFEST.json" `
  "STRATEGY_FACTORY_PHASE01_QA_REPORT.json" `
  "STRATEGY_FACTORY_PHASE01_FILE_INDEX.txt" `
  "STRATEGY_FACTORY_PHASE01_FILE_HASHES.sha256" `
  "COMMIT_MESSAGE.md"

git commit `
  -m "feat(alpha-lab): implement MQL5-first Strategy Factory contracts" `
  -m "Add the primary MQL5 canonical contract kernel, causal timestamp and stable identity rules, bar and anatomy event records, typed feature snapshots, artifact lineage, deterministic codecs, schema registry, Python research mirror, cross-language golden vectors, MetaEditor self-test harness, Obsidian documentation, QA, and phase handoff."

git push
```
