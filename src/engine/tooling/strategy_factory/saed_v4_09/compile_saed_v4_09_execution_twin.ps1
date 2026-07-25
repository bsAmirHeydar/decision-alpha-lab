$ErrorActionPreference = "Stop"
python src/engine/tooling/strategy_factory/saed_v4_09/run_saed_v4_09_full_qa.py
Write-Host "Repository QA passed. MetaEditor compilation remains an explicit Windows external gate."
