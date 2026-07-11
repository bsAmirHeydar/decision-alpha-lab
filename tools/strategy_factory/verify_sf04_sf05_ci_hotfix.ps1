$ErrorActionPreference = "Stop"
python tools/engineering/validate_alpha_lab_policy.py .
python docs/ai_algorithm_engineering_os/tools/validate_vault.py docs/ai_algorithm_engineering_os
python tools/engineering/check_mql5_compatibility.py .
python tools/engineering/audit_repository_layout.py .
